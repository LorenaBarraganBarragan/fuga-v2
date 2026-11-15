"""Expenses domain package for FUGA+."""

from app.domain.expenses.amount_parser import MontoResultado, extraer_monto
from app.domain.expenses.classifier import ClasificacionResultado, clasificar
from app.domain.expenses.date_parser import FechaResultado, extraer_fecha
from app.domain.expenses.diccionario_v1 import (
    CATEGORIAS,
    DICCIONARIO_VERSION,
    GENERICAS,
    REGLAS_VERSION,
)
from app.domain.expenses.interpreter import Draft, ValidacionError, interpretar
from app.domain.expenses.normalizer import normalizar, normalizar_descripcion

__all__ = [
    "Draft",
    "ValidacionError",
    "interpretar",
    "extraer_monto",
    "MontoResultado",
    "extraer_fecha",
    "FechaResultado",
    "clasificar",
    "ClasificacionResultado",
    "normalizar",
    "normalizar_descripcion",
    "CATEGORIAS",
    "GENERICAS",
    "DICCIONARIO_VERSION",
    "REGLAS_VERSION",
]
