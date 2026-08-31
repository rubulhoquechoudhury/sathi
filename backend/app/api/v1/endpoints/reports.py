"""
Citizen landslide report submission & retrieval endpoints.
"""

import uuid
from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.database.models import CitizenReport
from app.schemas.citizen import CitizenReportCreate, CitizenReportResponse

router = APIRouter()


@router.post("/reports", response_model=CitizenReportResponse, status_code=status.HTTP_201_CREATED)
def submit_citizen_report(
    payload: CitizenReportCreate,
    db: Session = Depends(get_db)
) -> CitizenReportResponse:
    """Submit a new citizen landslide observation report."""
    report_id = f"rep_{uuid.uuid4().hex[:10]}"

    report_db = CitizenReport(
        report_id=report_id,
        latitude=payload.latitude,
        longitude=payload.longitude,
        reporter_name=payload.reporter_name,
        severity=payload.severity,
        description=payload.description,
        status="PENDING"
    )
    db.add(report_db)
    db.commit()
    db.refresh(report_db)

    return report_db


@router.get("/reports", response_model=List[CitizenReportResponse])
def list_citizen_reports(
    limit: int = 50,
    db: Session = Depends(get_db)
) -> List[CitizenReportResponse]:
    """Retrieve submitted citizen landslide reports."""
    reports = (
        db.query(CitizenReport)
        .order_by(CitizenReport.created_at.desc())
        .limit(limit)
        .all()
    )
    return reports
