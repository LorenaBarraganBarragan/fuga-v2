"""
test_interpreter.py — Pruebas unitarias del motor determinista (F5)
Corpus obligatorio de 42 casos (§22.4 del Plan Maestro) y pruebas de determinismo.
"""

from datetime import date, timedelta
from zoneinfo import ZoneInfo
import pytest

from app.domain.expenses.interpreter import Draft, ValidacionError, interpretar
from app.domain.expenses.amount_parser import extraer_monto
from app.domain.expenses.date_parser import extraer_fecha
from app.domain.expenses.classifier import clasificar
from app.domain.expenses.normalizer import normalizar

ZONA = ZoneInfo("America/Bogota")


def _hoy() -> date:
    from datetime import datetime
    return datetime.now(tz=ZONA).date()


def _ayer() -> date:
    return _hoy() - timedelta(days=1)


# ============================================================================
# Corpus obligatorio de 42 casos (§22.4)
# ============================================================================

def test_caso_01():
    d = interpretar("Hoy gasté $8.000 en un taxi")
    assert d.monto_cop == 8000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Transporte"
    assert "taxi" in d.descripcion


def test_caso_02():
    d = interpretar("Ayer pagué 12500 de almuerzo")
    assert d.monto_cop == 12500
    assert d.fecha_gasto == _ayer()
    assert d.categoria_nombre == "Alimentación"
    assert "almuerzo" in d.descripcion


def test_caso_03():
    d = interpretar("Mercado 45000")
    assert d.monto_cop == 45000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Alimentación"
    assert "mercado" in d.descripcion


def test_caso_04():
    d = interpretar("Uber al trabajo 9.500")
    assert d.monto_cop == 9500
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Transporte"
    assert "uber" in d.descripcion


def test_caso_05():
    d = interpretar("Pagué el recibo de luz 32000")
    assert d.monto_cop == 32000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Servicios"
    assert "luz" in d.descripcion


def test_caso_06():
    d = interpretar("Netflix 16900")
    assert d.monto_cop == 16900
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Entretenimiento"
    assert "netflix" in d.descripcion


def test_caso_07():
    d = interpretar("Compré una camisa en 60000")
    assert d.monto_cop == 60000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Compras"
    assert "camisa" in d.descripcion


def test_caso_08():
    d = interpretar("Medicina 23000")
    assert d.monto_cop == 23000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Salud"
    assert "medicina" in d.descripcion


def test_caso_09():
    d = interpretar("Curso de inglés 120000")
    assert d.monto_cop == 120000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Educación"
    assert "ingles" in d.descripcion or "curso" in d.descripcion


def test_caso_10():
    d = interpretar("Arriendo 800000")
    assert d.monto_cop == 800000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Vivienda"
    assert "arriendo" in d.descripcion


def test_caso_11():
    d = interpretar("Gasté 5000 en algo")
    assert d.monto_cop == 5000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Otros"


def test_caso_12():
    d = interpretar("Taxi 8000")
    assert d.monto_cop == 8000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Transporte"
    assert "taxi" in d.descripcion


def test_caso_13():
    d = interpretar("8000 taxi")
    assert d.monto_cop == 8000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Transporte"
    assert "taxi" in d.descripcion


def test_caso_14():
    d = interpretar("COP 8.000 taxi")
    assert d.monto_cop == 8000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Transporte"
    assert "taxi" in d.descripcion


def test_caso_15():
    d = interpretar("8.000 pesos de taxi")
    assert d.monto_cop == 8000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Transporte"
    assert "taxi" in d.descripcion


def test_caso_16():
    d = interpretar("Ayer 3.500 bus")
    assert d.monto_cop == 3500
    assert d.fecha_gasto == _ayer()
    assert d.categoria_nombre == "Transporte"
    assert "bus" in d.descripcion


def test_caso_17_decimal_invalido():
    d = interpretar("Almuerzo 8,50")
    assert d.monto_cop is None
    assert any("decimal" in a.lower() for a in d.avisos)


def test_caso_18_monto_cero():
    d = interpretar("0 en nada")
    assert d.monto_cop is None


def test_caso_19_monto_negativo():
    d = interpretar("Taxi -5000")
    # Los montos negativos no son válidos para el parser COP
    assert d.monto_cop is None or d.monto_cop == 5000  # si se limpia el signo, pero -5000 no debe aceptarse como negativo


def test_caso_20_fuera_de_rango():
    d = interpretar("Gasté 100000001")
    assert d.monto_cop is None


def test_caso_21_vacio():
    with pytest.raises(ValidacionError):
        interpretar("")
    with pytest.raises(ValidacionError):
        interpretar("   ")


def test_caso_22_longitud_excedida():
    texto_largo = "a" * 281
    with pytest.raises(ValidacionError):
        interpretar(texto_largo)


def test_caso_23():
    d = interpretar("Café 4000")
    assert d.monto_cop == 4000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Alimentación"
    assert "cafe" in d.descripcion


def test_caso_24():
    d = interpretar("Cine 25000")
    assert d.monto_cop == 25000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Entretenimiento"
    assert "cine" in d.descripcion


def test_caso_25():
    d = interpretar("Transporte 3000")
    assert d.monto_cop == 3000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Transporte"


def test_caso_26():
    d = interpretar("Domicilio 18000")
    assert d.monto_cop == 18000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Alimentación"


def test_caso_27():
    d = interpretar("Farmacia 12000")
    assert d.monto_cop == 12000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Salud"


def test_caso_28():
    d = interpretar("Universidad 250000")
    assert d.monto_cop == 250000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Educación"


def test_caso_29():
    d = interpretar("Internet 89900")
    assert d.monto_cop == 89900
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Servicios"


def test_caso_30():
    d = interpretar("Zapatos 150000")
    assert d.monto_cop == 150000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Compras"


def test_caso_31_ambiguedad():
    d = interpretar("Hoy gasté $8.000 en un taxi y $5.000 en café")
    # Ambigüedad: múltiples montos sin autosuma, exige revisión
    assert d.monto_cop is None
    assert len(d.ambiguedades) > 0


def test_caso_32():
    d = interpretar("Fecha 15/03 taxi 7000")
    assert d.monto_cop == 7000
    assert d.categoria_nombre == "Transporte"
    assert d.fecha_gasto.month == 3
    assert d.fecha_gasto.day == 15


def test_caso_33():
    d = interpretar("2025-12-01 arriendo 800000")
    assert d.monto_cop == 800000
    assert d.fecha_gasto == date(2025, 12, 1)
    assert d.categoria_nombre == "Vivienda"


def test_caso_34_manana():
    d = interpretar("Mañana taxi 8000")
    assert d.monto_cop == 8000
    assert d.fecha_gasto == _hoy()
    assert any("mañana" in a.lower() or "futura" in a.lower() for a in d.avisos)
    assert d.categoria_nombre == "Transporte"


def test_caso_35_sin_monto():
    d = interpretar("Ayer")
    assert d.monto_cop is None
    assert any("monto" in a.lower() for a in d.avisos)


def test_caso_36():
    d = interpretar("Pagué 4500 de transmilenio")
    assert d.monto_cop == 4500
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Transporte"
    assert "transmilenio" in d.descripcion


def test_caso_37():
    d = interpretar("Snacks 2500")
    assert d.monto_cop == 2500
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Alimentación"


def test_caso_38():
    d = interpretar("Regalo 45000")
    assert d.monto_cop == 45000
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Compras"


def test_caso_39():
    d = interpretar("Spotify 14900")
    assert d.monto_cop == 14900
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Entretenimiento"


def test_caso_40():
    d = interpretar("Agua 2500")
    assert d.monto_cop == 2500
    assert d.fecha_gasto == _hoy()
    assert d.categoria_nombre == "Alimentación"


def test_caso_41_generico_gasto():
    d = interpretar("Gasto 5000")
    assert d.monto_cop == 5000
    assert d.categoria_nombre == "Otros"


def test_caso_42_generico_compra():
    d = interpretar("Compra 9000")
    assert d.monto_cop == 9000
    assert d.categoria_nombre == "Otros"


# ============================================================================
# Determinismo y memoria
# ============================================================================

def test_determinismo():
    texto = "Hoy gasté $8.000 en un taxi al trabajo"
    d1 = interpretar(texto)
    d2 = interpretar(texto)
    assert d1.monto_cop == d2.monto_cop
    assert d1.fecha_gasto == d2.fecha_gasto
    assert d1.categoria_nombre == d2.categoria_nombre
    assert d1.descripcion == d2.descripcion
    assert d1.confianza == d2.confianza
    assert d1.avisos == d2.avisos
    assert d1.ambiguedades == d2.ambiguedades


def test_draft_to_dict():
    d = interpretar("Hoy gasté $8.000 en un taxi")
    res = d.to_dict()
    assert "draft" in res
    assert res["draft"]["monto_cop"] == 8000
    assert res["draft"]["categoria_nombre"] == "Transporte"
    assert "confianza" in res
    assert "diccionario_version" in res
    assert "reglas_version" in res
