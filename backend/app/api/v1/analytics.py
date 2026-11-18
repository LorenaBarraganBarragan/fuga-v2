from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.security import CurrentUser, require_user
from app.db.session import get_db
from app.schemas.analytics import AnalyticsByCategoryResponse, AnalyticsSummaryResponse
from app.services.analytics_service import AnalyticsService

router = APIRouter(prefix="/analytics", tags=["analytics"])


def current_month():
    return datetime.now(ZoneInfo("America/Bogota")).strftime("%Y-%m")


@router.get("/summary", response_model=AnalyticsSummaryResponse)
def get_analytics_summary(
    periodo: str | None = None,
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    return AnalyticsService.get_summary(user.user_id, periodo or current_month(), db)


@router.get("/by-category", response_model=AnalyticsByCategoryResponse)
def get_analytics_by_category(
    periodo: str | None = None,
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    return AnalyticsService.get_by_category(user.user_id, periodo or current_month(), db)


@router.get("/comparison")
def compare(
    periodo: str | None = None,
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    return AnalyticsService.compare(user.user_id, periodo or current_month(), db)
