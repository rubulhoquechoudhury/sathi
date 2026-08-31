"""Pydantic API schemas."""
from app.schemas.health import HealthCheckResponse
from app.schemas.landslide import (
    LocationInput,
    TerrainInput,
    RainfallInput,
    LandslidePredictionRequest,
    LandslidePredictionResponse,
    AssessmentLogResponse
)
from app.schemas.citizen import CitizenReportCreate, CitizenReportResponse

__all__ = [
    "HealthCheckResponse",
    "LocationInput",
    "TerrainInput",
    "RainfallInput",
    "LandslidePredictionRequest",
    "LandslidePredictionResponse",
    "AssessmentLogResponse",
    "CitizenReportCreate",
    "CitizenReportResponse"
]
