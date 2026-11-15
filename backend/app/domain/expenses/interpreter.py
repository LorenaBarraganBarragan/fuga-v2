"""
interpreter.py — Orquestador del motor determinista para FUGA+

Integra normalizer, amount_parser, date_parser y classifier para
producir un Draft completo a partir de texto libre.

Reglas (D-05, RN-INT-01…08):
  - El borrador vive SOLO en memoria; este módulo no persiste nada.
  - Todos los campos del borrador son editables por el usuario.
  - La confianza general es el nivel más bajo entre los campos.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from typing import Optional

from app.domain.expenses.amount_parser import extraer_monto
from app.domain.expenses.classifier import clasificar
from app.domain.expenses.date_parser import extraer_fecha
from app.domain.expenses.diccionario_v1 import DICCIONARIO_VERSION, REGLAS_VERSION
from app.domain.expenses.normalizer import normalizar, normalizar_descripcion

TEXTO_MIN = 1
TEXTO_MAX = 280

# Muletillas que se eliminan para extraer la descripción limpia
_MULETILLAS_DESC = re.compile(
    r"\b(hoy|ayer|ma[ñn]ana|gaste|pagué|pague|compre|compré|"
    r"en un|en una|en|un|una|de|del|al)\b",
    re.IGNORECASE,
)
_MONTOS_PATTERN = re.compile(
    r"(?:\$\s*|\bCOP\s*)?\d[\d.]*(?:\s*pesos?)?"
    r"|\d+\s*[kK]\b",
    re.IGNORECASE,
)
_FECHAS_PATTERN = re.compile(
    r"\b\d{4}-\d{2}-\d{2}\b"
    r"|\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b"
    r"|\b\d{1,2}\s+de\s+(?:enero|febrero|marzo|abril|mayo|junio|"
    r"julio|agosto|septiembre|octubre|noviembre|diciembre)\b",
    re.IGNORECASE,
)


@dataclass
class Draft:
    """Borrador estructurado producido por el intérprete."""
    # Campos de negocio
    texto_entrada: str           # Input original (no se persiste en MVP)
    monto_cop: Optional[int]
    fecha_gasto: date
    descripcion: str             # Núcleo semántico extraído, editable
    categoria_nombre: str
    categoria_id: Optional[str]
    moneda: str = "COP"

    # Metadatos de confianza y avisos
    confianza: dict[str, str] = field(default_factory=dict)
    avisos: list[str] = field(default_factory=list)
    ambiguedades: list[str] = field(default_factory=list)

    # Versiones del motor
    diccionario_version: str = DICCIONARIO_VERSION
    reglas_version: str = REGLAS_VERSION

    def to_dict(self) -> dict:
        return {
            "draft": {
                "texto": self.texto_entrada,
                "monto_cop": self.monto_cop,
                "fecha_gasto": self.fecha_gasto,
                "descripcion": self.descripcion,
                "categoria_id": self.categoria_id,
                "categoria_nombre": self.categoria_nombre,
                "moneda": self.moneda,
            },
            "confianza": self.confianza,
            "avisos": self.avisos,
            "ambiguedades": self.ambiguedades,
            "diccionario_version": self.diccionario_version,
            "reglas_version": self.reglas_version,
        }


class ValidacionError(Exception):
    """El texto no cumple las restricciones básicas (vacío, muy largo, etc.)."""
    def __init__(self, mensaje: str, campo: str = "texto"):
        super().__init__(mensaje)
        self.campo = campo
        self.mensaje = mensaje


def _extraer_descripcion(texto: str, monto_str: Optional[str] = None) -> str:
    """
    Extrae el núcleo semántico: elimina muletillas, montos y fechas,
    y recorta a 120 caracteres.
    """
    t = texto.strip()
    # Eliminar montos
    t = _MONTOS_PATTERN.sub(" ", t)
    # Eliminar fechas
    t = _FECHAS_PATTERN.sub(" ", t)
    # Eliminar muletillas
    t = _MULETILLAS_DESC.sub(" ", t)
    # Normalizar y limpiar espacios
    t = normalizar(t)
    t = re.sub(r"\s+", " ", t).strip()

    # Si queda vacío, usar el texto completo normalizado truncado
    if not t:
        t = normalizar(texto)[:120]

    return t[:120] if t else "sin descripcion"


def interpretar(
    texto: str,
    catalogo_ids: Optional[dict[str, str]] = None,
) -> Draft:
    """
    Convierte texto libre en un Draft estructurado.

    Args:
        texto: Texto del gasto (máx. 280 caracteres).
        catalogo_ids: {nombre_categoria: uuid} de la BD (None en modo prueba).

    Returns:
        Draft completo con confianza, avisos y ambigüedades.

    Raises:
        ValidacionError: Si el texto es vacío, demasiado largo o solo espacios.

    >>> d = interpretar("Hoy gasté $8.000 en un taxi")
    >>> d.monto_cop
    8000
    >>> d.categoria_nombre
    'Transporte'
    """
    # --- Validaciones básicas de entrada ---
    if not isinstance(texto, str) or not texto.strip():
        raise ValidacionError("El texto no puede estar vacío.", campo="texto")

    if len(texto) > TEXTO_MAX:
        raise ValidacionError(
            f"El texto supera los {TEXTO_MAX} caracteres ({len(texto)}).",
            campo="texto",
        )

    if len(texto.strip()) < TEXTO_MIN:
        raise ValidacionError("El texto no puede estar vacío.", campo="texto")

    avisos: list[str] = []
    ambiguedades: list[str] = []

    # --- Extracción de monto ---
    res_monto = extraer_monto(texto)
    if res_monto.ambiguo:
        ambiguedades.extend(res_monto.avisos)
    elif res_monto.avisos:
        avisos.extend(res_monto.avisos)

    # --- Extracción de fecha ---
    res_fecha = extraer_fecha(texto)
    if res_fecha.avisos:
        avisos.extend(res_fecha.avisos)

    # --- Clasificación de categoría ---
    res_cat = clasificar(texto, catalogo_ids=catalogo_ids)
    if res_cat.avisos:
        avisos.extend(res_cat.avisos)

    # --- Extracción de descripción ---
    descripcion = _extraer_descripcion(texto)

    # --- Confianza general ---
    niveles_num = {"alta": 3, "media": 2, "baja": 1, "invalido": 0}
    confianza_dict = {
        "monto": res_monto.confianza if res_monto.monto is not None else "baja",
        "fecha": res_fecha.confianza,
        "categoria": res_cat.confianza,
        "descripcion": "media",  # Siempre extraída; el usuario la revisa
    }

    return Draft(
        texto_entrada=texto,
        monto_cop=res_monto.monto,
        fecha_gasto=res_fecha.fecha,
        descripcion=descripcion,
        categoria_nombre=res_cat.categoria_nombre,
        categoria_id=res_cat.categoria_id,
        moneda="COP",
        confianza=confianza_dict,
        avisos=avisos,
        ambiguedades=ambiguedades,
        diccionario_version=DICCIONARIO_VERSION,
        reglas_version=REGLAS_VERSION,
    )
