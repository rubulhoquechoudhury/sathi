"""
Pydantic V2 Schemas for Operational Dashboard Endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class StatCardItem(BaseModel):
    label: str
    value: str
    delta: str
    tone: str


class ZoneSummaryItem(BaseModel):
    district: str
    flood: int
    landslide: int
    status: str


class AlertItem(BaseModel):
    type: str
    title: str
    time: str
    severity: str
    description: str


class TrendDataItem(BaseModel):
    label: str
    value: int


class DashboardOverviewResponse(BaseModel):
    stat_cards: List[StatCardItem]
    zone_summary: List[ZoneSummaryItem]
    alerts: List[AlertItem]
    trend_data: List[TrendDataItem]
    recommendations: List[str]
