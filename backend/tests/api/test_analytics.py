"""
test_analytics.py — Pruebas de endpoints de analítica y agregados (HU-20, HU-21, F7)
"""

import uuid
from app.api.v1.analytics import get_analytics_summary, get_analytics_by_category
from app.core.security import CurrentUser


def test_get_analytics_summary():
    uid = uuid.uuid4()
    user = CurrentUser(user_id=uid, email="test@fuga.plus", rol="usuario")
    res = get_analytics_summary(periodo="2026-11", user=user)

    assert res.periodo == "2026-11"
    assert res.monto_total_cop >= 0
    assert res.cantidad_gastos >= 0
    assert res.promedio_gasto_cop >= 0


def test_get_analytics_by_category():
    uid = uuid.uuid4()
    user = CurrentUser(user_id=uid, email="test@fuga.plus", rol="usuario")
    res = get_analytics_by_category(periodo="2026-11", user=user)

    assert res.periodo == "2026-11"
    assert len(res.items) == 9
    cat_nombres = [item.categoria_nombre for item in res.items]
    assert "Alimentación" in cat_nombres
    assert "Transporte" in cat_nombres
    assert "Otros" in cat_nombres
