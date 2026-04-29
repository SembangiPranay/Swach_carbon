"""
Configuration and logging setup
"""
import os
import logging
import json
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()


class Config:
    """Application configuration"""

    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

    # Server
    DEBUG = os.getenv("DEBUG", "False").lower() == "true"
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 8000))

    # CORS
    ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

    # Timeouts
    AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", 300))  # 5 minutes
    LLM_TIMEOUT = int(os.getenv("LLM_TIMEOUT", 60))  # 1 minute

    # Rate limiting
    RATE_LIMIT_ENABLED = os.getenv("RATE_LIMIT_ENABLED", "True").lower() == "true"
    RATE_LIMIT_PER_MINUTE = int(os.getenv("RATE_LIMIT_PER_MINUTE", 10))

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        required = ["GROQ_API_KEY", "TAVILY_API_KEY", "GEMINI_API_KEY"]
        missing = [key for key in required if not getattr(cls, key)]

        if missing:
            raise ValueError(f"Missing required environment variables: {', '.join(missing)}")

        return True


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging"""

    def format(self, record):
        log_obj = {
            "timestamp": datetime.now().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
        }

        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj)


def setup_logging():
    """Configure logging with JSON formatter"""

    # Create logger
    logger = logging.getLogger("swach_ai")
    logger.setLevel(logging.DEBUG if Config.DEBUG else logging.INFO)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(JSONFormatter())
    logger.addHandler(console_handler)

    # File handler (if DEBUG)
    if Config.DEBUG:
        # Create logs directory
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, "swach_ai.log")
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(JSONFormatter())
        logger.addHandler(file_handler)

    return logger


# Initialize logger
logger = setup_logging()

# Create reports directory
reports_dir = os.path.join(os.path.dirname(__file__), "reports")
os.makedirs(reports_dir, exist_ok=True)

# Verify config on startup
try:
    Config.validate()
    logger.info("✓ Configuration validated successfully")
except ValueError as e:
    logger.error(f"Configuration error: {e}")
    raise
