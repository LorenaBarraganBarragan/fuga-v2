import pytest

from app.core.errors import ValidationException
from app.services.analytics_service import AnalyticsService, month_bounds


@pytest.mark.parametrize("period", ["2026-13", "2026-00", "2019-12", "bad", "2999-01"])
def test_period_validation(period):
    with pytest.raises(ValidationException):
        month_bounds(period)


def test_http_summary(private_client, monkeypatch):
    monkeypatch.setattr(
        AnalyticsService, "rows", lambda uid, p, db: [{"monto_cop": 100}, {"monto_cop": 101}]
    )
    res = private_client.get("/api/v1/analytics/summary?periodo=2026-01")
    assert res.status_code == 200
    assert res.json()["monto_total_cop"] == 201
    assert res.json()["promedio_gasto_cop"] == 101
