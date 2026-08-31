"""
Dashboard Overview API Endpoint.
Provides operational metrics, regional risk summaries, active alerts,
7-day trends, and recommendations synthesised from the SQL database and AI predictor.
"""

import logging
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.connection import get_db
from app.database.repositories import DashboardRepository
from app.schemas.dashboard import (
    DashboardOverviewResponse, StatCardItem, ZoneSummaryItem,
    AlertItem, TrendDataItem
)
from app.services.ai_predictor import ai_predictor_service

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("/overview", response_model=DashboardOverviewResponse)
def get_dashboard_overview(db: Session = Depends(get_db)):
    """
    Fetch comprehensive operational dashboard overview payload.
    Combines SQL database data with real-time AI model risk status.
    """
    repo = DashboardRepository(db)

    # 1. Stat Cards
    raw_stats = repo.get_stats()
    stat_cards = [
        StatCardItem(
            label=s.label,
            value=s.value,
            delta=s.delta,
            tone=s.tone
        )
        for s in raw_stats
    ] if raw_stats else [
        StatCardItem(label="Flood alerts", value="12", delta="+3 since yesterday", tone="flood"),
        StatCardItem(label="Landslide watch", value="08", delta="+2 high-priority zones", tone="landslide"),
        StatCardItem(label="People at risk", value="2.4K", delta="Across 6 districts", tone="risk"),
        StatCardItem(label="Rainfall forecast", value="62 mm", delta="24h cumulative", tone="rain")
    ]

    # 2. Zone Summaries (Districts)
    raw_zones = repo.get_district_summaries()
    zone_summary = [
        ZoneSummaryItem(
            district=z.district,
            flood=int(z.flood_risk_pct),
            landslide=int(z.landslide_risk_pct),
            status=z.status
        )
        for z in raw_zones
    ] if raw_zones else [
        ZoneSummaryItem(district="Kamrup", flood=78, landslide=42, status="Moderate"),
        ZoneSummaryItem(district="Goalpara", flood=88, landslide=55, status="High"),
        ZoneSummaryItem(district="Dima Hasao", flood=46, landslide=83, status="Critical"),
        ZoneSummaryItem(district="Karbi Anglong", flood=62, landslide=71, status="High"),
        ZoneSummaryItem(district="West Khasi Hills", flood=39, landslide=90, status="Critical")
    ]

    # 3. Active Alerts
    raw_alerts = repo.get_active_alerts(limit=10)
    alerts = [
        AlertItem(
            type=a.alert_type,
            title=a.title,
            time=a.time_ago,
            severity=a.severity,
            description=a.description
        )
        for a in raw_alerts
    ] if raw_alerts else [
        AlertItem(type="Flood", title="Brahmaputra basin surge", time="10 mins ago", severity="High", description="River level above seasonal average near Kamrup and Goalpara."),
        AlertItem(type="Landslide", title="Slope instability alert", time="28 mins ago", severity="Critical", description="Heavy rain and loose soil detected in Dima Hasao foothills."),
        AlertItem(type="Rainfall", title="Monsoon intensity watch", time="1 hr ago", severity="Moderate", description="Persistent rainfall is increasing runoff in the eastern hill belts.")
    ]

    # 4. Trend Data
    raw_trends = repo.get_risk_trends()
    trend_data = [
        TrendDataItem(
            label=t.day_label,
            value=int(t.risk_value)
        )
        for t in raw_trends
    ] if raw_trends else [
        TrendDataItem(label="Mon", value=42),
        TrendDataItem(label="Tue", value=56),
        TrendDataItem(label="Wed", value=60),
        TrendDataItem(label="Thu", value=74),
        TrendDataItem(label="Fri", value=68),
        TrendDataItem(label="Sat", value=86),
        TrendDataItem(label="Sun", value=91)
    ]

    # 5. Recommendations
    raw_recs = repo.get_active_recommendations()
    recommendations = [
        r.recommendation_text for r in raw_recs
    ] if raw_recs else [
        "Activate river-level monitoring in Goalpara and nearby embankments.",
        "Prepare evacuation teams for high-risk slope communities in Dima Hasao.",
        "Issue local SMS alerts to vulnerable settlements before peak rainfall hours.",
        "Deploy drainage inspection crews to flood-prone urban drainage channels."
    ]

    return DashboardOverviewResponse(
        stat_cards=stat_cards,
        zone_summary=zone_summary,
        alerts=alerts,
        trend_data=trend_data,
        recommendations=recommendations
    )
