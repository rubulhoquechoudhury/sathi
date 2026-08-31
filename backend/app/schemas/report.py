"""Pydantic V2 Schemas for Citizen Reports & Risk Map."""
from typing import Optional, List
from pydantic import BaseModel, Field
from app.schemas.prediction import PredictionResponse


class CitizenReportCreate(BaseModel):
    latitude: float = Field(..., ge=-90.0, le=90.0)
    longitude: float = Field(..., ge=-180.0, le=180.0)
    severity: int = Field(default=3, ge=1, le=5)
    description: Optional[str] = None
    image_url: Optional[str] = None


class CitizenReportResponse(BaseModel):
    id: int
    latitude: float
    longitude: float
    severity: int
    description: Optional[str]
    image_url: Optional[str]
    created_at: str


class RiskMapResponse(BaseModel):
    timestamp: str
    locations: List[PredictionResponse]
