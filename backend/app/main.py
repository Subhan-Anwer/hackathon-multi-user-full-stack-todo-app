from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.db import create_db_and_tables
from .routes import tasks
from .middleware.auth import JWTMiddleware
from .config import settings
import os
from dotenv import load_dotenv
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle events."""
    # Startup
    logger.info("Initializing application...")

    # Validate required configuration
    if not settings.BETTER_AUTH_SECRET or settings.BETTER_AUTH_SECRET == "fallback-secret-for-testing":
        logger.warning("Using fallback auth secret. Please set BETTER_AUTH_SECRET environment variable.")

    if not settings.DATABASE_URL:
        logger.error("DATABASE_URL environment variable not set!")
        raise ValueError("DATABASE_URL environment variable is required")

    # Create database tables
    create_db_and_tables()

    logger.info(f"Application initialized with JWT expiry: {settings.access_token_expire_delta}")
    logger.info(f"Session warning threshold: {settings.session_warning_threshold_delta}")

    yield

    # Shutdown
    logger.info("Shutting down application...")

app = FastAPI(
    title="Todo API",
    description="Multi-user todo API with JWT authentication and session management",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT authentication middleware
app.add_middleware(JWTMiddleware)

# Include routers
app.include_router(tasks.router)

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        log_level="info" if settings.DEBUG else "warning"
    )
