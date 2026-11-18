"""
test_aggregations.py — Pruebas unitarias del cálculo de estadísticas (HU-20, HU-21, F7)
"""

from app.domain.analytics.aggregations import calcular_desglose_categorias, calcular_resumen


def test_calcular_resumen_periodo_vacio():
    res = calcular_resumen([], periodo="2026-11")
    assert res.periodo == "2026-11"
    assert res.monto_total_cop == 0
    assert res.cantidad_gastos == 0
    assert res.promedio_gasto_cop == 0


def test_calcular_resumen_con_gastos():
    gastos = [
        {"monto_cop": 8000},
        {"monto_cop": 12000},
        {"monto_cop": 25000},
    ]
    res = calcular_resumen(gastos, periodo="2026-11")
    assert res.monto_total_cop == 45000
    assert res.cantidad_gastos == 3
    assert res.promedio_gasto_cop == 15000


def test_calcular_resumen_redondeo_promedio():
    gastos = [
        {"monto_cop": 10000},
        {"monto_cop": 15000},
    ]  # Promedio 12500 exacto
    res = calcular_resumen(gastos, periodo="2026-11")
    assert res.promedio_gasto_cop == 12500

    gastos2 = [
        {"monto_cop": 10000},
        {"monto_cop": 11000},
        {"monto_cop": 10000},
    ]  # 31000 / 3 = 10333.333 -> 10333
    res2 = calcular_resumen(gastos2, periodo="2026-11")
    assert res2.promedio_gasto_cop == 10333


def test_calcular_desglose_categorias():
    cat_transporte = "10000000-0000-0000-0000-000000000002"
    cat_alimentacion = "10000000-0000-0000-0000-000000000001"

    gastos = [
        {"categoria_id": cat_transporte, "monto_cop": 10000},
        {"categoria_id": cat_transporte, "monto_cop": 10000},
        {"categoria_id": cat_alimentacion, "monto_cop": 20000},
    ]  # Total = 40000. Transporte = 20000 (50.0%), Alimentación = 20000 (50.0%)

    desglose = calcular_desglose_categorias(gastos, periodo="2026-11")
    assert len(desglose) == 9  # Las 9 categorías presentes

    transporte = next(d for d in desglose if d.categoria_nombre == "Transporte")
    assert transporte.monto_cop == 20000
    assert transporte.cantidad == 2
    assert transporte.porcentaje == 50.0

    alimentacion = next(d for d in desglose if d.categoria_nombre == "Alimentación")
    assert alimentacion.monto_cop == 20000
    assert alimentacion.cantidad == 1
    assert alimentacion.porcentaje == 50.0

    otros = next(d for d in desglose if d.categoria_nombre == "Otros")
    assert otros.monto_cop == 0
    assert otros.cantidad == 0
    assert otros.porcentaje == 0.0
