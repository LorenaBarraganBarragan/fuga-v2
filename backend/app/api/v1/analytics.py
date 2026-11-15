"""
analytics.py — Endpoints del dashboard analítico y estadísticas (HU-20, HU-21)
"""

from datetime import datetime
from typing import Optional
from zoneinfo import ZoneInfo
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import CurrentUser, get_current_user
from app.schemas.analytics import AnalyticsByCategoryResponse, AnalyticsSummaryResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])
ZONA = ZoneInfo("America/Bogota")


def _periodo_actual() -> str:
    return datetime.now(tz=ZONA).strftime("%Y-%m")


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_analytics_summary(
    periodo: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}$", description="Formato YYYY-MM"),
    user: CurrentUser = Depends(get_current_user),
    db: Optional[Session] = Depends(lambda: None),
):
    """Retorna total acumulado, cantidad y promedio en COP para el periodo."""
    p = periodo or _periodo_actual()
    return AnalyticsService.get_summary(usuario_id=user.user_id, periodo=p, db=db)


@router.get("/by-category", response_model=AnalyticsByCategoryResponse)
def get_analytics_by_category(
    periodo: Optional[str] = Query(None, pattern=r"^\d{4}-\d{2}$", description="Formato YYYY-MM"),
    user: CurrentUser = Depends(get_current_user),
    db: Optional[Session] = Depends(lambda: None),
):
    """Retorna el desglose de gastos por categoría para el periodo."""
    p = periodo or _periodo_actual()
    return AnalyticsService.get_by_category(usuario_id=user.user_id, periodo=p, db=db)
