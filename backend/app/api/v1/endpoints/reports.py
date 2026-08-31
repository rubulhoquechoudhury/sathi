"""Citizen Reports API Endpoint."""
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.repositories import CitizenReportRepository
from app.schemas.report import CitizenReportCreate, CitizenReportResponse

router = APIRouter()


@router.post("", response_model=CitizenReportResponse, status_code=status.HTTP_201_CREATED)
def submit_citizen_report(report: CitizenReportCreate, db: Session = Depends(get_db)):
    """
    Submit citizen report.
    Stored for monitoring & dashboard display, but strictly EXCLUDED from predictive AI model input.
    """
    repo = CitizenReportRepository(db)
    rep = repo.create_report(
        lat=report.latitude,
        lon=report.longitude,
        severity=report.severity,
        description=report.description or "",
        image_url=report.image_url
    )
    return CitizenReportResponse(
        id=rep.id,
        latitude=rep.latitude,
        longitude=rep.longitude,
        severity=rep.severity,
        description=rep.description,
        image_url=rep.image_url,
        created_at=rep.created_at.isoformat()
    )


@router.get("", response_model=List[CitizenReportResponse])
def get_citizen_reports(limit: int = 50, db: Session = Depends(get_db)):
    """Fetch citizen reports."""
    repo = CitizenReportRepository(db)
    reports = repo.get_all(limit=limit)
    return [
        CitizenReportResponse(
            id=r.id,
            latitude=r.latitude,
            longitude=r.longitude,
            severity=r.severity,
            description=r.description,
            image_url=r.image_url,
            created_at=r.created_at.isoformat()
        )
        for r in reports
    ]
