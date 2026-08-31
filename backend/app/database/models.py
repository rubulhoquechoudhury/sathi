"""
SQLAlchemy ORM database models for risk assessments and citizen reports.
"""

from datetime import datetime, timezone
from sqlalchemy import Column, Integer, Float, String, DateTime, Text
from app.database.session import Base


class LandslideAssessment(Base):
    """Database model for logging AI landslide risk predictions."""
    __tablename__ = "landslide_assessments"

    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(String, unique=True, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(String, nullable=True)
    landslide_probability = Column(Float, nullable=False)
    risk_score = Column(Integer, nullable=False)
    risk_level = Column(String, nullable=False)
    raw_input_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)


class CitizenReport(Base):
    """Database model for citizen-submitted landslide observations."""
    __tablename__ = "citizen_reports"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(String, unique=True, index=True, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    reporter_name = Column(String, nullable=True)
    severity = Column(Integer, default=1, nullable=False)  # 1 (Low) to 3 (Critical)
    description = Column(Text, nullable=True)
    status = Column(String, default="PENDING", nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
