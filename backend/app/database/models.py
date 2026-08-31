"""
SQLAlchemy ORM Models for SATHI Landslide Early-Warning Backend System.
Matches Section 4 & Database Tables specification of Master Prompt.
"""

from datetime import datetime, timezone
from typing import Optional
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Index, Text, UniqueConstraint
)
from sqlalchemy.orm import relationship
from app.database.connection import Base


def utc_now():
    return datetime.now(timezone.utc)


class MonitoredLocation(Base):
    """Monitored Spatial Locations for Landslide Risk Evaluation."""
    __tablename__ = "monitored_locations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    predictions = relationship("RiskPrediction", back_populates="location")


class Sensor(Base):
    """IoT Sensors deployed across monitored zones."""
    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sensor_id = Column(String(100), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    sensor_type = Column(String(100), default="rain_gauge", nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=utc_now, nullable=False)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now, nullable=False)

    readings = relationship("SensorReading", back_populates="sensor")


class SensorReading(Base):
    """Ingested IoT Sensor Readings (Rainfall, Soil Moisture, Temp, Humidity)."""
    __tablename__ = "sensor_readings"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    sensor_id = Column(String(100), ForeignKey("sensors.sensor_id"), nullable=False, index=True)
    rainfall_mm = Column(Float, nullable=True)
    soil_moisture = Column(Float, nullable=True)
    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    recorded_at = Column(DateTime, default=utc_now, nullable=False, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    sensor = relationship("Sensor", back_populates="readings")

    __table_args__ = (
        Index("idx_sensor_reading_time", "sensor_id", "recorded_at"),
        UniqueConstraint("sensor_id", "recorded_at", name="uq_sensor_reading_time"),
    )


class WeatherObservation(Base):
    """Gridded or Station Weather Observations (1h, 24h, 3d, 7d, 14d Rainfall & Soil)."""
    __tablename__ = "weather_observations"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)

    rain_1h = Column(Float, default=0.0, nullable=False)
    rain_24h = Column(Float, default=0.0, nullable=False)
    rain_3d = Column(Float, default=0.0, nullable=False)
    rain_7d = Column(Float, default=0.0, nullable=False)
    rain_14d = Column(Float, default=0.0, nullable=False)

    temperature = Column(Float, nullable=True)
    humidity = Column(Float, nullable=True)
    soil_moisture = Column(Float, nullable=True)

    observed_at = Column(DateTime, default=utc_now, nullable=False, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    __table_args__ = (
        Index("idx_weather_coords_time", "latitude", "longitude", "observed_at"),
    )


class CitizenReport(Base):
    """Citizen Landslide Reports (Stored for Monitoring & Confirmation, Excluded from AI Input)."""
    __tablename__ = "citizen_reports"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)
    severity = Column(Integer, default=1, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)


class RiskPrediction(Base):
    """Historical & Real-Time AI Landslide Risk Predictions."""
    __tablename__ = "risk_predictions"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    location_id = Column(Integer, ForeignKey("monitored_locations.id"), nullable=True, index=True)
    latitude = Column(Float, nullable=False, index=True)
    longitude = Column(Float, nullable=False, index=True)

    landslide_probability = Column(Float, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String(50), nullable=False)  # LOW, MODERATE, HIGH, CRITICAL
    data_status = Column(String(50), default="ALPHAEARTH_UNAVAILABLE", nullable=False)
    model_version = Column(String(50), default="xgb-v1", nullable=False)

    prediction_timestamp = Column(DateTime, default=utc_now, nullable=False, index=True)
    created_at = Column(DateTime, default=utc_now, nullable=False)

    location = relationship("MonitoredLocation", back_populates="predictions")

    __table_args__ = (
        Index("idx_risk_pred_loc_time", "location_id", "prediction_timestamp"),
        Index("idx_risk_pred_lat_lon", "latitude", "longitude"),
    )
