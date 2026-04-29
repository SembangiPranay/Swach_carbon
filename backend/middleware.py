"""
Middleware for CORS, request logging, and rate limiting
"""
import time
from typing import Dict, Tuple
from collections import defaultdict
from datetime import datetime, timedelta
from fastapi import Request
from fastapi.responses import JSONResponse
from config import logger, Config


class RateLimiter:
    """Token bucket rate limiter per IP"""

    def __init__(self, requests_per_minute: int = 10):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, list] = defaultdict(list)

    def is_allowed(self, client_ip: str) -> Tuple[bool, Dict]:
        """Check if request is allowed, return (allowed, info)"""
        now = datetime.now()
        cutoff = now - timedelta(minutes=1)

        # Clean old requests
        self.requests[client_ip] = [
            req_time for req_time in self.requests[client_ip] if req_time > cutoff
        ]

        # Check limit
        if len(self.requests[client_ip]) >= self.requests_per_minute:
            return False, {
                "remaining": 0,
                "reset_after": 60,
            }

        # Add this request
        self.requests[client_ip].append(now)

        return True, {
            "remaining": self.requests_per_minute - len(self.requests[client_ip]),
            "reset_after": 60,
        }


rate_limiter = RateLimiter(requests_per_minute=Config.RATE_LIMIT_PER_MINUTE)


async def cors_middleware(request: Request, call_next):
    """CORS middleware"""
    response = await call_next(request)

    # Add CORS headers
    origin = request.headers.get("origin", "*")
    if origin in Config.ALLOWED_ORIGINS or "*" in Config.ALLOWED_ORIGINS:
        response.headers["Access-Control-Allow-Origin"] = origin
        response.headers["Access-Control-Allow-Credentials"] = "true"
        response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
        response.headers[
            "Access-Control-Allow-Headers"
        ] = "Content-Type, Authorization, X-Requested-With"

    return response


async def rate_limit_middleware(request: Request, call_next):
    """Rate limiting middleware"""
    if not Config.RATE_LIMIT_ENABLED:
        return await call_next(request)

    # Get client IP
    client_ip = request.client.host if request.client else "unknown"

    # Check rate limit (allow /health endpoint)
    if request.url.path != "/health":
        allowed, info = rate_limiter.is_allowed(client_ip)

        if not allowed:
            logger.warning(f"Rate limit exceeded for {client_ip}")
            return JSONResponse(
                status_code=429,
                content={
                    "error": "Too Many Requests",
                    "detail": f"Rate limit: {Config.RATE_LIMIT_PER_MINUTE} requests per minute",
                    "retry_after": info["reset_after"],
                },
            )

        # Add rate limit headers
        response = await call_next(request)
        response.headers["X-RateLimit-Remaining"] = str(info["remaining"])
        response.headers["X-RateLimit-Reset"] = str(info["reset_after"])
        return response

    return await call_next(request)


async def logging_middleware(request: Request, call_next):
    """Request/response logging middleware"""
    start_time = time.time()

    # Log request
    logger.info(
        f"→ {request.method} {request.url.path} from {request.client.host if request.client else 'unknown'}"
    )

    try:
        response = await call_next(request)
    except Exception as e:
        logger.error(f"✗ Request failed: {str(e)}")
        raise

    # Log response
    process_time = time.time() - start_time
    logger.info(
        f"← {request.method} {request.url.path} {response.status_code} ({process_time:.2f}s)"
    )

    response.headers["X-Process-Time"] = str(process_time)
    return response


async def handle_options(request: Request):
    """Handle CORS preflight OPTIONS requests"""
    return JSONResponse(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )
