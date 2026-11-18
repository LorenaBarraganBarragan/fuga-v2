"""Conceptos generales: misma representación en interpretación y análisis histórico."""

from copy import deepcopy
from datetime import date
from uuid import uuid4

import pytest
from pydantic import ValidationError

from app.domain.expenses.diccionario_v1 import (
    DICCIONARIO_VERSION,
    EQUIVALENCIAS,
    JUSTIFICACIONES_EQUIVALENCIAS,
    NORMALIZACION_VERSION,
    REGLAS_VERSION,
)
from app.domain.expenses.interpreter import interpretar
from app.domain.expenses.normalizer import normalizar_descripcion
from app.domain.leaks.grouping import agrupar_gastos
from app.domain.leaks.rule_fuga_01 import PARAMETROS_DEFAULT_V1_0, evaluar_fuga_01
from app.schemas.expenses import ExpenseCreate


@pytest.mark.parametrize(
    ("text", "amount", "concept"),
    [
        ("Gasté 5000 en café", 5000, "cafe"),
        ("Compré un café de 5000", 5000, "cafe"),
        ("Pagué 5000 por un café", 5000, "cafe"),
        ("Hoy compré café por 5000", 5000, "cafe"),
        ("Gasté 3000 en buseta", 3000, "buseta"),
        ("Pagué 3000 de buseta", 3000, "buseta"),
        ("Tomé una buseta de 3000", 3000, "buseta"),
        ("Compré una recarga de celular", None, "recarga celular"),
        ("Pagué comida para perro", None, "comida perro"),
        ("  ¡HOY, GASTÉ: COP 5.000 EN CAFÉ!  ", 5000, "cafe"),
        ("Gasté 5.000 en café", 5000, "cafe"),
        ("Compré un café de 5.000.", 5000, "cafe"),
        ("Compré un café de COP5000", 5000, "cafe"),
        ("Pagué 3k de buseta", 3000, "buseta"),
        ("Café 5000", 5000, "cafe"),
        ("Yo pagué 800000 por el arriendo", 800000, "arriendo"),
        ("Compré un cuaderno de 8000", 8000, "cuaderno"),
        ("Pagué 25000 por consulta médica", 25000, "consulta medica"),
        ("Compré una camiseta por $30.000", 30000, "camiseta"),
        ("Pagué 20000 por una entrada de cine", 20000, "entrada cine"),
        ("He pagado 89900 por servicio de internet", 89900, "internet"),
        ("Pagué 3000 por una fotocopia", 3000, "fotocopias"),
        ("Adquirí una recarga para celular por 10000", 10000, "recarga celular"),
        ("Gasté 15000 en alimento para perro", 15000, "comida perro"),
        ("Pagué 4000 por un boleto de bus", 4000, "pasaje bus"),
        ("Pagué 800000 por alquiler de vivienda", 800000, "arriendo vivienda"),
        ("Compré café espresso por 5000", 5000, "cafe expreso"),
        ("2026-11-14 gasté 5000 en café", 5000, "cafe"),
        ("Gasté 5000 en café el 14 de noviembre", 5000, "cafe"),
        ("Gasté 5000 en café con leche", 5000, "cafe con leche"),
        ("CAFÉ-CON-LECHE", None, "cafe con leche"),
        ("Tomé una buseta intermunicipal de 5000", 5000, "buseta intermunicipal"),
        ("Compré vitamina B12 por 5000", 5000, "vitamina b12"),
        ("Compré 2 cuadernos por 10000", 10000, "2 cuadernos"),
        ("Pagué 5000 por un bus ruta 5000", 5000, "bus ruta 5000"),
        ("Plan de 5000", 10000, "plan de 5000"),
        ("Plan de 5000", 5000, "plan de 5000"),
        ("Compré en El Corral por 5000", 5000, "el corral"),
        ("Pagué 5000 por comida a la carta", 5000, "comida a la carta"),
    ],
)
def test_general_canonical_concepts(text, amount, concept):
    assert normalizar_descripcion(text, amount) == concept
    assert normalizar_descripcion(concept, amount) == concept


@pytest.mark.parametrize(
    ("left", "right"),
    [
        ("café", "café con leche"),
        ("café", "café sin azúcar"),
        ("café con leche", "café sin leche"),
        ("buseta", "bus intermunicipal"),
        ("buseta", "buseta intermunicipal"),
        ("recarga celular", "recarga de tarjeta de transporte"),
        ("comida perro", "comida para gato"),
        ("comida perro", "comida para perro adulto"),
        ("leche con lactosa", "leche sin lactosa"),
        ("vitamina B12", "vitamina B6"),
        ("iphone 15", "iphone 16"),
        ("modelo 5000", "modelo 6000"),
        ("plan de 300 minutos", "plan de 500 minutos"),
        ("no compre cafe", "cafe"),
        ("seguro de vida", "seguro de vehiculo"),
        ("alquiler de vivienda", "alquiler de carro"),
    ],
)
def test_qualifiers_negation_and_numbers_do_not_merge(left, right):
    assert normalizar_descripcion(left, 5000) != normalizar_descripcion(right, 5000)


def test_every_equivalence_is_explicit_justified_and_idempotent():
    assert EQUIVALENCIAS.keys() == JUSTIFICACIONES_EQUIVALENCIAS.keys()
    for alias, target in EQUIVALENCIAS.items():
        assert JUSTIFICACIONES_EQUIVALENCIAS[alias].strip()
        assert normalizar_descripcion(alias) == target
        assert normalizar_descripcion(target) == target


def test_long_concepts_are_bounded_and_idempotent_without_losing_original_input():
    raw = "Compré " + "material artesanal " * 12
    original = raw
    concept = normalizar_descripcion(raw)
    assert 1 <= len(concept) <= 120
    assert normalizar_descripcion(concept) == concept
    assert raw == original


@pytest.mark.parametrize(
    ("text", "expected", "category"),
    [
        ("Gasté 5000 en café", "cafe", "Alimentación"),
        ("Compré un café de 5000", "cafe", "Alimentación"),
        ("Pagué 5000 por un café", "cafe", "Alimentación"),
        ("Hoy compré café por 5000", "cafe", "Alimentación"),
        ("Tomé una buseta de 3000", "buseta", "Transporte"),
        ("Compré una recarga de celular", "recarga celular", "Servicios"),
        ("Pagué comida para perro", "comida perro", "Alimentación"),
        ("Pagué 25000 por consulta médica", "consulta medica", "Salud"),
        ("Compré un cuaderno de 8000", "cuaderno", "Educación"),
        ("Pagué 800000 por arriendo", "arriendo", "Vivienda"),
        ("Compré una camiseta por 30000", "camiseta", "Compras"),
        ("Pagué 20000 por entrada de cine", "entrada cine", "Entretenimiento"),
        ("Pagué 5000 por troquelado artesanal", "troquelado artesanal", "Otros"),
    ],
)
def test_interpreter_shares_concept_and_preserves_original_text(text, expected, category):
    draft = interpretar(text)
    assert draft.descripcion == expected
    assert draft.categoria_nombre == category
    assert draft.texto_entrada == text
    assert draft.to_dict()["draft"]["texto"] == text
    assert draft.diccionario_version == "1.1"
    assert draft.reglas_version == "1.1"


def coffee_rows(descriptions=None):
    descriptions = descriptions or ["gaste cafe", "cafe", "cafe", "por cafe"]
    category = str(uuid4())
    return [
        {
            "id": str(uuid4()),
            "categoria_id": category,
            "descripcion": description,
            "monto_cop": 5000,
            "fecha_gasto": date(2026, 11, day),
            "deleted_at": None,
        }
        for day, description in zip((14, 15, 17, 18), descriptions, strict=False)
    ]


def test_exact_four_user_descriptions_form_one_leak_without_mutating_records():
    expenses = coffee_rows()
    original = deepcopy(expenses)
    result = evaluar_fuga_01(expenses, fecha_referencia=date(2026, 11, 18))
    assert len(result) == 1
    assert result[0].descripcion_normalizada == "cafe"
    assert result[0].ocurrencias == 4
    assert result[0].monto_acumulado_cop == 20000
    assert result[0].regla_version == "1.0"
    assert set(result[0].evidencia_gasto_ids) == {row["id"] for row in expenses}
    assert expenses == original


@pytest.mark.parametrize(
    ("descriptions", "concept"),
    [
        (["gaste 5000 en buseta", "pague 5000 de buseta", "tome una buseta de 5000"], "buseta"),
        (["recarga de celular", "recarga para celular", "recarga celular"], "recarga celular"),
        (["comida para perro", "comida de perro", "alimento para perro"], "comida perro"),
        (["compre un cuaderno", "pague 5000 por cuaderno", "cuaderno"], "cuaderno"),
        (
            ["gaste 5000 en consulta medica", "pague consulta medica", "consulta médica"],
            "consulta medica",
        ),
        (["compre una camiseta", "camiseta", "pague 5000 por camiseta"], "camiseta"),
        (["entrada de cine", "boleta de cine", "entrada cine"], "entrada cine"),
        (
            ["arriendo de vivienda", "alquiler de vivienda", "arriendo vivienda"],
            "arriendo vivienda",
        ),
    ],
)
def test_rule_groups_equivalent_concepts_across_categories(descriptions, concept):
    expenses = coffee_rows(descriptions)
    result = evaluar_fuga_01(expenses, fecha_referencia=date(2026, 11, 18))
    assert len(result) == 1
    assert result[0].descripcion_normalizada == concept
    assert result[0].monto_acumulado_cop == 15000


def test_same_concept_in_different_categories_stays_separate():
    expenses = coffee_rows()
    for row in expenses[2:]:
        row["categoria_id"] = "another-category"
    assert len(agrupar_gastos(expenses)) == 2
    assert evaluar_fuga_01(expenses, fecha_referencia=date(2026, 11, 18)) == []


@pytest.mark.parametrize(
    ("first", "second"),
    [
        ("cafe", "cafe con leche"),
        ("buseta", "bus intermunicipal"),
        ("vitamina B12", "vitamina B6"),
        ("comida perro", "comida para gato"),
    ],
)
def test_distinct_concepts_cannot_create_a_leak_by_combining_their_counts(first, second):
    expenses = coffee_rows([first, second, first, second])
    assert len(agrupar_gastos(expenses)) == 2
    assert evaluar_fuga_01(expenses, fecha_referencia=date(2026, 11, 18)) == []


def test_new_normalization_never_bypasses_existing_thresholds():
    expenses = coffee_rows()
    for row in expenses:
        row["fecha_gasto"] = date(2026, 11, 18)
    assert evaluar_fuga_01(expenses, fecha_referencia=date(2026, 11, 18)) == []
    assert PARAMETROS_DEFAULT_V1_0 == {
        "ventana_dias": 30,
        "min_gastos": 3,
        "min_fechas": 3,
        "monto_min": 1000,
        "monto_max": 30000,
        "suma_min": 15000,
        "zona": "America/Bogota",
    }
    assert (DICCIONARIO_VERSION, REGLAS_VERSION, NORMALIZACION_VERSION) == ("1.1", "1.1", "1.1")


@pytest.mark.parametrize("version", ["1.0", "1.1"])
def test_old_and_new_confirmation_versions_preserve_description(version):
    description = "Pagué comida para perro"
    expense = ExpenseCreate(
        monto_cop=5000,
        categoria_id=uuid4(),
        descripcion=description,
        fecha_gasto=date(2026, 11, 14),
        diccionario_version=version,
        reglas_version=version,
    )
    assert expense.descripcion == description


def test_legacy_default_versions_and_invalid_combinations():
    fields = {
        "monto_cop": 5000,
        "descripcion": "cafe",
        "categoria_id": uuid4(),
        "fecha_gasto": date(2026, 11, 14),
    }
    assert ExpenseCreate(**fields).diccionario_version == "1.0"
    with pytest.raises(ValidationError):
        ExpenseCreate(**fields, diccionario_version="1.1", reglas_version="1.0")
    with pytest.raises(ValidationError):
        ExpenseCreate(**fields, diccionario_version="99", reglas_version="99")
