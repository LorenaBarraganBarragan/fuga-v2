"""Catálogo base inmutable 1.0 y extensión de interpretación/normalización 1.1."""

import json
from pathlib import Path
from typing import Any

_NORMALIZACION: dict[str, Any] = json.loads(
    Path(__file__).with_name("normalizacion_v1_1.json").read_text(encoding="utf-8")
)
_DATA: dict[str, Any] = json.loads(
    Path(__file__).with_name(_NORMALIZACION["base_categorias"]).read_text(encoding="utf-8")
)
DICCIONARIO_VERSION: str = _NORMALIZACION["version"]
REGLAS_VERSION: str = _NORMALIZACION["reglas_version"]
NORMALIZACION_VERSION: str = _NORMALIZACION["version"]
VERSIONES_COMPATIBLES = frozenset({("1.0", "1.0"), (DICCIONARIO_VERSION, REGLAS_VERSION)})
CATEGORIAS: dict[str, dict] = {
    key: {
        **category,
        "keywords": category["keywords"] + _NORMALIZACION["keywords_adicionales"].get(key, []),
    }
    for key, category in _DATA["categorias"].items()
}
GENERICAS: list[str] = _DATA["genericas"] + _NORMALIZACION["genericas_adicionales"]
# No se inventan equivalencias: solo se aplican entradas aprobadas en el JSON versionado.
EQUIVALENCIAS: dict[str, str] = _NORMALIZACION["equivalencias"]
JUSTIFICACIONES_EQUIVALENCIAS: dict[str, str] = _NORMALIZACION["justificaciones_equivalencias"]
PREFIJOS_TEMPORALES: list[str] = _NORMALIZACION["prefijos_temporales"]
PREFIJOS_TRANSACCION: list[str] = _NORMALIZACION["prefijos_transaccion"]
CONECTORES_INICIALES: list[str] = _NORMALIZACION["conectores_iniciales"]
FRASES_PROTEGIDAS: list[str] = _NORMALIZACION["frases_protegidas"]
