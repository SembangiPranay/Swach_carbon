"""
FastAPI Backend for Swach AI Carbon Agent

Exposes the ReAct agent as REST API with:
- POST /calculate - Start calculation
- GET /stream?id=uuid - SSE stream of agent thoughts
- GET /report?id=uuid - Download PDF
- GET /health - Health check
"""

from fastapi import FastAPI, BackgroundTasks, Query, HTTPException
from fastapi.responses import StreamingResponse, FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import asyncio
from datetime import datetime
from typing import Optional

# Import our modules
from config import Config, logger
from models import (
    ActivityDataRequest,
    CalculationResponse,
    HealthResponse,
    StreamEventType,
)
from streaming import stream_manager, StreamEventType as StreamType
from middleware import cors_middleware, rate_limit_middleware, logging_middleware
from agent import CarbonFootprintAgent

# Initialize FastAPI app
app = FastAPI(
    title="Swach AI Carbon Agent API",
    description="ReAct agent for carbon footprint analysis with GHG Protocol compliance",
    version="1.0.0",
)

# Add middleware (order matters!)
app.middleware("http")(logging_middleware)
app.middleware("http")(rate_limit_middleware)
app.middleware("http")(cors_middleware)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def run_agent_background(calc_id: str, activity_data: dict):
    """Background task: Run agent and emit streaming events"""
    try:
        logger.info(f"[{calc_id}] Starting agent execution...")

        # Create agent
        agent = CarbonFootprintAgent(model="groq", verbose=False)

        # Emit initial thought
        stream_manager.add_event(
            calc_id,
            StreamType.THOUGHT,
            "Starting carbon footprint analysis for your company...",
        )

        # Emit calculation step
        stream_manager.add_event(
            calc_id,
            StreamType.ACTION,
            f"Calculating emissions for {activity_data.get('company_name', 'Company')}...",
        )

        # Run agent (this returns output text)
        try:
            result = agent.run(activity_data)

            # Parse results if possible
            stream_manager.add_event(
                calc_id,
                StreamType.OBSERVATION,
                "Analysis complete. Generating report...",
            )

            # Emit results
            stream_manager.complete_calculation(
                calc_id,
                results={
                    "status": "success",
                    "message": result,
                    "timestamp": datetime.now().isoformat(),
                },
                pdf_path=f"backend/reports/{calc_id}.pdf",
            )

            logger.info(f"[{calc_id}] ✓ Agent execution complete")

        except Exception as agent_error:
            logger.error(f"[{calc_id}] Agent error: {agent_error}")
            stream_manager.fail_calculation(calc_id, str(agent_error))

    except Exception as e:
        logger.error(f"[{calc_id}] Background task error: {e}")
        stream_manager.fail_calculation(calc_id, str(e))


from fastapi import UploadFile, File
from tools.vision_analyzer import UtilityBillAnalyzer

@app.post("/analyze-bill")
async def analyze_bill_endpoint(bill_type: str = "electricity", file: UploadFile = File(...)):
    """Analyze an uploaded utility bill image"""
    try:
        # Save file temporarily
        temp_path = f"backend/assets/temp_{file.filename}"
        os.makedirs("backend/assets", exist_ok=True)
        with open(temp_path, "wb") as buffer:
            buffer.write(await file.read())
            
        analyzer = UtilityBillAnalyzer()
        result = analyzer.analyze_bill(temp_path, bill_type)
        
        # Cleanup
        try:
            os.remove(temp_path)
        except:
            pass
            
        return JSONResponse(content=json.loads(result))
    except Exception as e:
        logger.error(f"Error in /analyze-bill: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/calculate", response_model=CalculationResponse)
async def calculate_emissions(
    data: ActivityDataRequest, background_tasks: BackgroundTasks
):
    """
    Start a carbon emissions calculation

    Returns a calculation_id that can be used to stream results and get the report
    """
    try:
        # Create calculation
        calc_id = stream_manager.create_calculation(data.company_name)

        # Convert Pydantic model to dict
        activity_data = data.model_dump()

        # Queue background task
        background_tasks.add_task(run_agent_background, calc_id, activity_data)

        logger.info(f"✓ Calculation queued: {calc_id}")

        return CalculationResponse(calculation_id=calc_id)

    except Exception as e:
        logger.error(f"Error in /calculate: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/stream")
async def stream_results(id: str = Query(..., description="Calculation ID from /calculate")):
    """
    Stream agent thoughts and analysis progress via Server-Sent Events

    Use this endpoint to show real-time agent reasoning in the frontend
    """
    try:
        # Verify calculation exists
        calc = stream_manager.get_calculation(id)
        if not calc:
            raise HTTPException(status_code=404, detail="Calculation not found")

        logger.info(f"[{id}] SSE stream opened")

        async def event_generator():
            """Generate SSE events"""
            last_event_count = 0

            try:
                while True:
                    # Get all events
                    events = stream_manager.get_events(id)

                    # Send new events since last check
                    for event in events[last_event_count:]:
                        yield event.to_sse_format()
                        last_event_count += 1

                    # Check if complete
                    calc = stream_manager.get_calculation(id)
                    if calc and calc.status in ["complete", "failed"]:
                        logger.info(f"[{id}] ✓ SSE stream complete")
                        break

                    # Wait before checking again
                    await asyncio.sleep(0.5)

            except asyncio.CancelledError:
                logger.info(f"[{id}] SSE stream cancelled by client")

        return StreamingResponse(event_generator(), media_type="text/event-stream")

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in /stream: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/report")
async def get_report(id: str = Query(..., description="Calculation ID from /calculate")):
    """
    Download the generated PDF report

    Call this after receiving 'complete' event from /stream
    """
    try:
        # Verify calculation exists
        calc = stream_manager.get_calculation(id)
        if not calc:
            raise HTTPException(status_code=404, detail="Calculation not found")

        # Check if report is ready
        if calc.status == "running":
            raise HTTPException(status_code=202, detail="Report still generating")

        if calc.status == "failed":
            raise HTTPException(status_code=400, detail=f"Calculation failed: {calc.error}")

        # Check if PDF exists
        pdf_path = calc.pdf_path
        if not pdf_path or not os.path.exists(pdf_path):
            raise HTTPException(status_code=404, detail="Report file not found")

        logger.info(f"[{id}] ✓ Report downloaded")

        return FileResponse(
            path=pdf_path,
            filename=f"carbon_report_{id}.pdf",
            media_type="application/pdf",
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in /report: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint for monitoring

    Returns server status and service availability
    """
    try:
        # Check services
        services = {
            "groq": "✓ configured",
            "tavily": "✓ configured",
            "gemini": "✓ configured",
            "database": "✓ ok",
        }

        # Try Groq
        if not os.getenv("GROQ_API_KEY"):
            services["groq"] = "✗ missing key"

        # Try Tavily
        if not os.getenv("TAVILY_API_KEY"):
            services["tavily"] = "✗ missing key"

        # Try Gemini
        if not os.getenv("GEMINI_API_KEY"):
            services["gemini"] = "✗ missing key"

        stats = stream_manager.get_stats()

        return HealthResponse(
            status="healthy",
            timestamp=datetime.now().isoformat(),
            services=services,
        )

    except Exception as e:
        logger.error(f"Error in /health: {e}")
        return HealthResponse(
            status="degraded",
            timestamp=datetime.now().isoformat(),
            services={"error": str(e)},
        )


@app.options("/{path_name:path}")
async def options_handler(path_name: str):
    """Handle CORS preflight OPTIONS requests"""
    return JSONResponse(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
            "Access-Control-Allow-Headers": "Content-Type, Authorization",
        },
    )


@app.get("/stats")
async def get_stats():
    """Get stream manager statistics"""
    return stream_manager.get_stats()


@app.on_event("startup")
async def startup_event():
    """Run on app startup"""
    logger.info("="*70)
    logger.info("SWACH AI CARBON AGENT API - Starting Up")
    logger.info("="*70)

    # Verify config
    try:
        Config.validate()
        logger.info("✓ Configuration validated")
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        raise

    # Create required directories
    os.makedirs("backend/reports", exist_ok=True)
    logger.info("✓ Directories ready")

    logger.info("✓ API ready at http://localhost:8000/docs")


@app.on_event("shutdown")
async def shutdown_event():
    """Run on app shutdown"""
    logger.info("Shutting down API...")
    stream_manager.cleanup_expired()
    logger.info("Cleanup complete")


# Error handler
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    logger.error(f"{exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle uncaught exceptions"""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if logger else "Unknown error",
        },
    )


if __name__ == "__main__":
    import uvicorn

    logger.info("Starting Uvicorn server...")
    uvicorn.run(
        app,
        host=Config.HOST,
        port=Config.PORT,
        log_level="info" if not Config.DEBUG else "debug",
    )
