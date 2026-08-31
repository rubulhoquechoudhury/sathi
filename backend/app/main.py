"""
SIH26001 Landslide Early-Warning Backend FastAPI Server.
Main entry point for starting the web service.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.database.session import init_db
from app.services.ai_predictor import get_ai_predictor
from app.api.v1.router import api_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("backend_main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan event handler executing startup and shutdown tasks."""
    logger.info("Initializing database tables...")
    init_db()

    logger.info("Pre-loading AI prediction model...")
    predictor = get_ai_predictor()
    if predictor.is_loaded:
        logger.info("AI Model loaded successfully into application state.")
    else:
        logger.warning(f"AI Model load failed on startup: {predictor.load_error}")

    yield
    logger.info("Shutting down backend server...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API v1 routes with /api/v1 prefix and root level alias for maximum frontend compatibility
app.include_router(api_router, prefix=settings.API_V1_STR)
app.include_router(api_router)


@app.get("/", tags=["Root"])
def root():
    """Root welcoming endpoint."""
    return {
        "message": "Welcome to SIH26001 Landslide Early-Warning Backend API",
        "docs_url": "/docs",
        "health_check": f"{settings.API_V1_STR}/health"
    }
