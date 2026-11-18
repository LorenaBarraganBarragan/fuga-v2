from datetime import date, timedelta

from app.domain.leaks.rule_fuga_01 import PARAMETROS_DEFAULT_V1_0
from app.services.leaks_service import empty_state


def test_no_expenses_is_empty_not_a_failure():
    assert empty_state([], PARAMETROS_DEFAULT_V1_0)[0] == "sin_gastos"


def test_insufficient_eligible_data_is_explicit():
    assert (
        empty_state(
            [{"monto_cop": 500, "descripcion": "taxi", "fecha_gasto": date(2026, 1, 1)}],
            PARAMETROS_DEFAULT_V1_0,
        )[0]
        == "datos_insuficientes"
    )


def test_no_pattern_is_different_from_insufficient_data():
    rows = [
        {
            "monto_cop": 1000,
            "descripcion": "taxi",
            "fecha_gasto": date(2026, 1, 1) + timedelta(days=i),
        }
        for i in range(3)
    ]
    assert empty_state(rows, PARAMETROS_DEFAULT_V1_0)[0] == "sin_posibles_fugas"
