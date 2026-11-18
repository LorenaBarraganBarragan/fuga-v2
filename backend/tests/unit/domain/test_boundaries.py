from datetime import date, timedelta
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.domain.analytics.aggregations import calcular_desglose_categorias, calcular_resumen
from app.domain.expenses.amount_parser import extraer_monto
from app.domain.leaks.rule_fuga_01 import evaluar_fuga_01
from app.schemas.expenses import ExpenseCreate


@pytest.mark.parametrize(
    "text", ["taxi USD 8000", "almuerzo 8 euros", "£ 8000", "taxi -8000", "taxi 8,50"]
)
def test_reject_invalid_money(text):
    assert extraer_monto(text).monto is None


def test_day_of_month_not_an_amount():
    assert extraer_monto("15 de noviembre taxi 8000").monto == 8000


def test_window_is_exactly_30_inclusive_dates():
    today = date(2026, 11, 15)
    category = str(uuid4())
    rows = [
        {
            "id": str(uuid4()),
            "categoria_id": category,
            "descripcion": "taxi",
            "monto_cop": 5000,
            "fecha_gasto": today - timedelta(days=d),
        }
        for d in (0, 1, 30)
    ]
    assert evaluar_fuga_01(rows, fecha_referencia=today) == []
    rows[2]["fecha_gasto"] = today - timedelta(days=29)
    assert len(evaluar_fuga_01(rows, fecha_referencia=today)) == 1


def test_empty_description_cannot_trigger():
    today = date(2026, 11, 15)
    rows = [
        {
            "id": str(uuid4()),
            "categoria_id": "cat",
            "descripcion": " ",
            "monto_cop": 5000,
            "fecha_gasto": today - timedelta(days=d),
        }
        for d in (0, 1, 2)
    ]
    assert evaluar_fuga_01(rows, fecha_referencia=today) == []


def test_half_up_and_database_category_ids():
    assert (
        calcular_resumen([{"monto_cop": 100}, {"monto_cop": 101}], "2026-01").promedio_gasto_cop
        == 101
    )
    cid = str(uuid4())
    items = calcular_desglose_categorias(
        [{"monto_cop": 100, "categoria_id": cid}],
        "2026-01",
        [{"id": cid, "nombre": "Transporte", "orden": 2}],
    )
    assert items[0].monto_cop == 100


@pytest.mark.parametrize("amount", [True, 1.1, 0, -1, 100000001, "8000"])
def test_confirmed_amount_must_be_strict_positive_integer(amount):
    with pytest.raises(ValidationError):
        ExpenseCreate(
            monto_cop=amount, descripcion="taxi", categoria_id=uuid4(), fecha_gasto=date(2026, 1, 1)
        )
