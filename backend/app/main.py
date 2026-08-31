"""
Main FastAPI Application Entry Point for SATHI Landslide Early-Warning Backend.
Configures lifespan, CORS, database initialization, AI model preloading,
background risk monitoring worker, REST API routers, and WebSockets.
"""

import logging
from datetime import datetime, timezone
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.database.connection import init_db
from app.services.ai_predictor import ai_predictor_service
from app.workers.risk_monitor import risk_monitor_worker
from app.websocket.manager import manager

# Route Imports
from app.api.v1.endpoints import predictions, sensors, weather, reports, risk, zones, model, inventory
from app.websocket import routes as ws_routes

setup_logging()
logger = logging.getLogger("backend_main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI Lifespan Context Manager."""
    logger.info("Initializing SATHI Backend Services...")

    # 1. Initialize DB tables if SQLite fallback
    init_db()

    # 2. Preload AI Model once
    ai_predictor_service.load_model()

    # 3. Start Background Risk Monitoring Worker
    risk_monitor_worker.start()

    logger.info("SATHI Backend initialized successfully!")
    yield

    # Shutdown
    await risk_monitor_worker.stop()
    logger.info("SATHI Backend shutdown complete.")




app = FastAPI(
    title=settings.PROJECT_NAME,
    description="SATHI Landslide Early-Warning Backend API & AI Engine",
    version=settings.MODEL_VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)


# CORS Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.parsed_cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Mounting REST Routers
app.include_router(predictions.router, prefix=f"{settings.API_V1_STR}/predictions", tags=["Predictions"])
app.include_router(sensors.router, prefix=f"{settings.API_V1_STR}/sensors", tags=["Sensors"])
app.include_router(weather.router, prefix=f"{settings.API_V1_STR}/weather", tags=["Weather"])
app.include_router(reports.router, prefix=f"{settings.API_V1_STR}/reports", tags=["Reports"])
app.include_router(risk.router, prefix=f"{settings.API_V1_STR}/risk", tags=["Risk"])
app.include_router(zones.router, prefix=f"{settings.API_V1_STR}", tags=["Zones"])
app.include_router(model.router, prefix=f"{settings.API_V1_STR}/model", tags=["Model"])
app.include_router(inventory.router, prefix=f"{settings.API_V1_STR}", tags=["Inventory"])

# Mount Native WebSocket Router
app.include_router(ws_routes.router, tags=["WebSockets"])


# Root Aliases for Frontend Compatibility
@app.get("/zones", tags=["Zones Alias"])
def get_zones_root_alias():
    return zones.get_risk_zones(ai_service=ai_predictor_service)

@app.get("/inventory/landslides", tags=["Inventory Alias"])
def get_inventory_landslides_root_alias(state: str = None, limit: int = 200, offset: int = 0):
    return inventory.get_landslide_inventory(state=state, limit=limit, offset=offset)

@app.get("/inventory/stats", tags=["Inventory Alias"])
def get_inventory_stats_root_alias():
    return inventory.get_inventory_stats()


@app.get("/health", tags=["Health"])
def health_check():
    """Health & Readiness Status Endpoint."""
    model_status = "loaded" if ai_predictor_service.is_loaded else "unavailable"
    version = ai_predictor_service.predictor.model_version if ai_predictor_service.is_loaded and ai_predictor_service.predictor else "unknown"

    return {
        "status": "ok",
        "database": "connected",
        "model": {
            "loaded": ai_predictor_service.is_loaded,
            "version": version
        },
        "websocket_clients": manager.client_count,
        "risk_monitor": {
            "running": risk_monitor_worker._running,
            "interval_seconds": settings.RISK_UPDATE_INTERVAL_SECONDS
        }
    }
