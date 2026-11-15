"""
test_rule_fuga_01.py — Matriz completa de pruebas para la regla FUGA-01 v1.0 (§22.6 del Plan Maestro)
"""

from datetime import date, timedelta
import uuid

from app.domain.leaks.rule_fuga_01 import evaluar_fuga_01

REF = date(2026, 11, 15)
CAT_TRANSPORTE = "10000000-0000-0000-0000-000000000002"
CAT_ALIMENTACION = "10000000-0000-0000-0000-000000000001"
CAT_OTROS = "10000000-0000-0000-0000-000000000009"


def _gasto(
    monto: int,
    dia_offset: int,
    desc: str = "cafe",
    cat: str = CAT_ALIMENTACION,
    deleted: bool = False,
) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "categoria_id": cat,
        "descripcion": desc,
        "monto_cop": monto,
        "fecha_gasto": REF - timedelta(days=dia_offset),
        "deleted_at": REF if deleted else None,
    }


def test_f01_borde_exacto_candidato():
    # 3 gastos, 3 fechas distintas, 5.000 c/u (suma 15.000)
    gastos = [
        _gasto(5000, 1),
        _gasto(5000, 2),
        _gasto(5000, 3),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 1
    assert res[0].ocurrencias == 3
    assert res[0].monto_acumulado_cop == 15000


def test_f02_suma_insuficiente():
    # Suma 14.999 -> Sin candidato
    gastos = [
        _gasto(5000, 1),
        _gasto(5000, 2),
        _gasto(4999, 3),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 0


def test_f03_fechas_insuficientes():
    # 3 gastos, pero solo 2 fechas distintas -> Sin candidato
    gastos = [
        _gasto(5000, 1),
        _gasto(5000, 1),
        _gasto(5000, 2),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 0


def test_f04_cantidad_insuficiente():
    # Solo 2 gastos -> Sin candidato
    gastos = [
        _gasto(10000, 1),
        _gasto(10000, 2),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 0


def test_f05_monto_menor_al_minimo():
    # Uno de 999 se descarta -> quedan solo 2 elegibles -> Sin candidato
    gastos = [
        _gasto(999, 1),
        _gasto(7000, 2),
        _gasto(8000, 3),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 0


def test_f06_monto_mayor_al_maximo():
    # Uno de 30.001 se descarta -> quedan solo 2 elegibles -> Sin candidato
    gastos = [
        _gasto(30001, 1),
        _gasto(7000, 2),
        _gasto(8000, 3),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 0


def test_f07_cuatro_gastos_tres_elegibles():
    # 4 gastos, 3 elegibles y 1 de 35.000 descartado -> Candidato con 3 ocurrencias
    gastos = [
        _gasto(5000, 1),
        _gasto(5000, 2),
        _gasto(5000, 3),
        _gasto(35000, 4),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 1
    assert res[0].ocurrencias == 3
    assert res[0].monto_acumulado_cop == 15000


def test_f08_misma_categoria_distinta_descripcion():
    # No se agrupan si la descripción no coincide
    gastos = [
        _gasto(5000, 1, desc="cafe"),
        _gasto(5000, 2, desc="almuerzo"),
        _gasto(5000, 3, desc="cena"),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 0


def test_f09_distinta_categoria_misma_descripcion():
    # Misma descripción pero en distintas categorías no se agrupan
    gastos = [
        _gasto(5000, 1, desc="snack", cat=CAT_ALIMENTACION),
        _gasto(5000, 2, desc="snack", cat=CAT_TRANSPORTE),
        _gasto(5000, 3, desc="snack", cat=CAT_ALIMENTACION),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 0


def test_f10_normalizacion_de_descripcion():
    # "Café", "  cafe ", "CAFÉ" deben agruparse
    gastos = [
        _gasto(5000, 1, desc="Café"),
        _gasto(5000, 2, desc="  cafe  "),
        _gasto(5000, 3, desc="CAFÉ"),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 1
    assert res[0].descripcion_normalizada == "cafe"
    assert res[0].ocurrencias == 3


def test_f11_descripcion_generica_descartada():
    # Descripción "gasto" es genérica -> descartada
    gastos = [
        _gasto(5000, 1, desc="gasto"),
        _gasto(5000, 2, desc="gasto"),
        _gasto(5000, 3, desc="gasto"),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 0


def test_f12_categoria_otros_con_descripcion_informativa():
    # Categoría Otros con descripción informativa sí es candidata válida
    gastos = [
        _gasto(5000, 1, desc="fotocopias", cat=CAT_OTROS),
        _gasto(5000, 2, desc="fotocopias", cat=CAT_OTROS),
        _gasto(5000, 3, desc="fotocopias", cat=CAT_OTROS),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 1
    assert res[0].categoria_id == CAT_OTROS
    assert res[0].descripcion_normalizada == "fotocopias"


def test_f13_gasto_con_deleted_at_excluido():
    # Un gasto con deleted_at no se cuenta
    gastos = [
        _gasto(5000, 1),
        _gasto(5000, 2),
        _gasto(5000, 3, deleted=True),
    ]
    res = evaluar_fuga_01(gastos, fecha_referencia=REF)
    assert len(res) == 0
