"""
amount_parser.py — Extracción determinista de montos en COP para FUGA+

Reglas (RN-INT-02 / RN-INT-03 / D-03):
  - Aceptar: 8000, 8.000, $8.000, $ 8.000, COP 8.000, 8.000 pesos, 8k (k = miles)
  - Rechazar: decimales con coma (8,50) o punto seguido de 1–2 dígitos (8.5, 8.50)
  - Rango válido: 1 … 100.000.000 (enteros COP)
  - Si hay múltiples montos → ambigüedad (se devuelve None + aviso)
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Optional


@dataclass(frozen=True)
class MontoResultado:
    monto: Optional[int]  # None si no encontró o hay ambigüedad
    confianza: str  # "alta" | "media" | "baja" | "invalido"
    avisos: list[str]
    ambiguo: bool


# --- Patrones -----------------------------------------------------------

# Prefijos opcionales: $, COP, cop
_PREFIX = r"(?:\$\s*|COP\s*|cop\s*)?"

# Número entero con separadores de miles opcionales (punto como separador de miles en es-CO)
# Acepta: 8000, 8.000, 80.000, 1.000.000
# RECHAZA: 8.5, 8.50, 8,50 (estos tienen 1–2 dígitos tras el separador)
_ENTERO = r"\b(\d{1,3}(?:\.\d{3})+(?!\d)|\d+)\b"

# Sufijos opcionales: "pesos", "cop"
_SUFFIX = r"(?:\s*(?:pesos?|cop))?"

# k/K como abreviatura de miles (8k → 8000)
_CON_K = r"\b(\d+(?:[.,]\d+)?)\s*[kK]\b"

# Decimal explícito — para detectar y RECHAZAR
_DECIMAL_COMA = r"\d+,\d{1,2}\b"
_DECIMAL_PUNTO = r"\d+\.\d{1,2}\b"  # 8.5 o 8.50 (punto seguido de 1-2 dígitos)

PATRON_MONTO = re.compile(rf"{_PREFIX}{_ENTERO}{_SUFFIX}", re.IGNORECASE)
PATRON_K = re.compile(rf"{_PREFIX}{_CON_K}", re.IGNORECASE)
PATRON_DECIMAL_COMA = re.compile(rf"\b{_DECIMAL_COMA}")
PATRON_DECIMAL_PUNTO = re.compile(
    r"\b(\d+)\.(\d{1,2})\b(?!\d)"  # punto seguido de exactamente 1-2 dígitos, no más
)
PATRON_NEGATIVO = re.compile(r"(?:^|[^\w])-\s*\$?\d+")

MONTO_MIN = 1
MONTO_MAX = 100_000_000


def _limpiar_monto_str(s: str) -> Optional[int]:
    """Convierte '8.000' → 8000, '1.000.000' → 1000000, '8000' → 8000."""
    # Remover puntos de miles (separador es-CO)
    limpio = s.replace(".", "")
    try:
        valor = int(limpio)
        return valor if MONTO_MIN <= valor <= MONTO_MAX else None
    except ValueError:
        return None


def extraer_monto(texto: str) -> MontoResultado:
    """
    Extrae el monto en COP de un texto libre.

    Returns MontoResultado con:
      - monto: int o None
      - confianza: "alta" | "media" | "invalido"
      - avisos: lista de mensajes
      - ambiguo: True si hay múltiples montos

    >>> extraer_monto("Hoy gasté $8.000 en un taxi")
    MontoResultado(monto=8000, confianza='alta', avisos=[], ambiguo=False)
    >>> extraer_monto("Almuerzo 12500").monto
    12500
    >>> extraer_monto("Taxi 8,50").monto is None
    True
    >>> extraer_monto("Taxi 8.5").monto is None
    True
    """
    avisos: list[str] = []
    texto_norm = texto.strip()
    if re.search(r"\b(?:USD|EUR|GBP|dolares|dólares|euros)\b|[€£]", texto_norm, re.IGNORECASE):
        return MontoResultado(None, "invalido", ["Solo se aceptan pesos colombianos (COP)."], False)

    # 1. Detectar negativos explícitos → rechazo inmediato
    if PATRON_NEGATIVO.search(texto_norm):
        return MontoResultado(
            monto=None,
            confianza="invalido",
            avisos=["Monto negativo detectado. Solo se aceptan montos enteros positivos en COP."],
            ambiguo=False,
        )

    # 2. Detectar decimales explícitos → rechazo inmediato (RN-INT-03)
    if PATRON_DECIMAL_COMA.search(texto_norm):
        return MontoResultado(
            monto=None,
            confianza="invalido",
            avisos=["Monto con decimal (coma) detectado. Solo se aceptan enteros en COP."],
            ambiguo=False,
        )

    # Detectar patrón X.YY donde Y tiene 1-2 dígitos (decimal con punto)
    # Excepto: 8.000 (3 dígitos) que es separador de miles
    for m in PATRON_DECIMAL_PUNTO.finditer(texto_norm):
        decimal_part = m.group(2)
        if len(decimal_part) < 3:
            return MontoResultado(
                monto=None,
                confianza="invalido",
                avisos=["Monto con decimal (punto) detectado. Solo se aceptan enteros en COP."],
                ambiguo=False,
            )

    # 3. Buscar montos con sufijo K
    montos_k: list[int] = []
    texto_sin_k = texto_norm
    for m in PATRON_K.finditer(texto_norm):
        raw = m.group(1).replace(",", ".")
        try:
            val = int((Decimal(raw) * 1000).quantize(Decimal("1"), rounding=ROUND_HALF_UP))
            if MONTO_MIN <= val <= MONTO_MAX:
                montos_k.append(val)
        except ValueError:
            pass
    texto_sin_k = PATRON_K.sub(" ", texto_sin_k)

    # 4. Buscar montos enteros normales
    # Excluir fechas: patrón DD/MM o YYYY-MM-DD no debe confundirse con monto
    texto_sin_fechas = re.sub(
        r"\b\d{4}-\d{2}-\d{2}\b|\b\d{1,2}/\d{1,2}(?:/\d{2,4})?\b",
        " ",
        texto_sin_k,
    )
    texto_sin_fechas = re.sub(
        r"\b\d{1,2}\s+de\s+[a-záéíóú]+\b", " ", texto_sin_fechas, flags=re.IGNORECASE
    )

    montos_enteros: list[int] = []
    for m in PATRON_MONTO.finditer(texto_sin_fechas):
        parsed_value = _limpiar_monto_str(m.group(1))
        if parsed_value is not None:
            montos_enteros.append(parsed_value)

    todos_montos = montos_k + montos_enteros

    if not todos_montos:
        return MontoResultado(
            monto=None,
            confianza="baja",
            avisos=["No se encontró un monto en el texto."],
            ambiguo=False,
        )

    # 4. Deduplicar (mismo valor repetido no es ambigüedad real)
    unicos = list(dict.fromkeys(todos_montos))

    if len(unicos) > 1:
        return MontoResultado(
            monto=None,
            confianza="invalido",
            avisos=[
                f"Se detectaron múltiples montos: {unicos}. "
                "Por favor ingresa solo un monto o corrige el texto."
            ],
            ambiguo=True,
        )

    monto = unicos[0]

    # Confianza alta si tiene prefijo explícito ($, COP) o sufijo "pesos"
    patron_explicito = re.compile(rf"(?:\$\s*|COP\s*){_ENTERO}|{_ENTERO}\s*pesos?", re.IGNORECASE)
    confianza = "alta" if patron_explicito.search(texto_sin_fechas) else "media"

    return MontoResultado(
        monto=monto,
        confianza=confianza,
        avisos=avisos,
        ambiguo=False,
    )
