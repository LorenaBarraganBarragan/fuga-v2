"""Normalización básica de texto y extracción canónica conservadora de conceptos 1.1.

La forma básica conserva puntuación para los analizadores de campos. La forma de
concepto elimina accesorios reconocidos y se comparte con la agrupación de FUGA-01.
"""

import re
import unicodedata
from decimal import Decimal, InvalidOperation


def normalizar(texto: str) -> str:
    """
    Normaliza un texto para comparación y clasificación:
    1. Strip de espacios extremos
    2. Minúsculas
    3. Eliminar diacríticos (tildes, diéresis)
    4. Colapsar espacios múltiples

    >>> normalizar("  Hoy Gasté $8.000 en un Táxi  ")
    'hoy gaste $8.000 en un taxi'
    >>> normalizar("Café con Leché")
    'cafe con leche'
    """
    if not isinstance(texto, str):
        raise TypeError(f"Se esperaba str, se recibió {type(texto)}")

    # Strip
    texto = texto.strip()
    # Minúsculas
    texto = texto.lower()
    # Eliminar diacríticos (NFD descompone, luego se filtran las marcas Mn)
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    # Colapsar espacios
    texto = re.sub(r"\s+", " ", texto)

    return texto


_NUMERO = r"\d+(?:[.,]\d+)*(?:\s*k)?"
_DINERO_EXPLICITO = re.compile(
    rf"(?:\b(?:por|de|a)\s+)?(?:"
    rf"(?<!\w)(?:\$\s*|cop\s*){_NUMERO}(?:\s*(?:pesos?|cop))?(?!\w)"
    rf"|(?<!\w){_NUMERO}\s*(?:pesos?|cop)\b)"
)
_COSTO_FINAL = re.compile(rf"\s+(?:por|de|a)\s+({_NUMERO})[\s.!?;,:]*$")
_COSTO_INICIAL = re.compile(rf"^({_NUMERO})\s+(?=(?:en|por|de)\b)")
_NUMERO_FINAL = re.compile(rf"(?:^|\s)({_NUMERO})$")
_FECHAS = re.compile(
    r"\b(?:fecha\s+)?(?:\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}(?:/\d{2,4})?)\b"
    r"|\b(?:el\s+)?\d{1,2}\s+de\s+(?:enero|febrero|marzo|abril|mayo|junio|julio|"
    r"agosto|septiembre|octubre|noviembre|diciembre)(?:\s+de\s+\d{4})?\b"
)
_NUMERO_IDENTIFICADOR = re.compile(
    r"\b(?:modelo|serie|ruta|linea|plan|talla|version|iphone|memoria|capacidad|dosis)"
    r"(?:\s+de)?\s*$"
)


def _mismo_importe(token: str, monto_cop: int) -> bool:
    value = token.replace(" ", "")
    try:
        if value.endswith("k"):
            return Decimal(value[:-1].replace(",", ".")) * 1000 == monto_cop
        return Decimal(value.replace(".", "").replace(",", ".")) == monto_cop
    except InvalidOperation:
        return False


def normalizar_descripcion(raw: str, monto_cop: int | None = None) -> str:
    """Extrae un concepto conservador, sin reescribir el gasto ni perder calificadores.

    Solo se eliminan conectores al inicio; los internos requieren una equivalencia
    explícita. Con/sin, negaciones, modelos y destinos permanecen diferenciados.
    """
    from app.domain.expenses.diccionario_v1 import (
        CONECTORES_INICIALES,
        EQUIVALENCIAS,
        FRASES_PROTEGIDAS,
        PREFIJOS_TEMPORALES,
        PREFIJOS_TRANSACCION,
    )

    text = _FECHAS.sub(" ", normalizar(raw))
    text = _DINERO_EXPLICITO.sub(" ", text)
    # Keep numeric attributes when they do not match the known expense amount.
    tail_cost = _COSTO_FINAL.search(text)
    if tail_cost and not _NUMERO_IDENTIFICADOR.search(text[: tail_cost.start()]):
        if monto_cop is None or _mismo_importe(tail_cost[1], monto_cop):
            text = text[: tail_cost.start()]
    prefixes = sorted(PREFIJOS_TEMPORALES + PREFIJOS_TRANSACCION, key=len, reverse=True)
    while True:
        previous = text
        # Preserve punctuation within numbers until monetary spans are removed.
        text = re.sub(r"(?<!\d)[^\w\s]|[^\w\s](?!\d)|_", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        if text.startswith("yo ") and any(
            text[3:] == prefix or text[3:].startswith(prefix + " ")
            for prefix in PREFIJOS_TRANSACCION
        ):
            text = text[3:]
        for prefix in prefixes:
            if text == prefix or text.startswith(prefix + " "):
                text = text[len(prefix) :].strip()
                break
        # A bare initial number is removed only with an explicit spending connector.
        text = _COSTO_INICIAL.sub("", text)
        if any(text == phrase or text.startswith(phrase + " ") for phrase in FRASES_PROTEGIDAS):
            break
        first, _, remainder = text.partition(" ")
        if first in CONECTORES_INICIALES:
            text = remainder
        if text == previous:
            break

    # An unmarked number is otherwise preserved unless it matches the known price.
    tail = _NUMERO_FINAL.search(text)
    if tail and monto_cop is not None and _mismo_importe(tail[1], monto_cop):
        before = text[: tail.start()].rstrip()
        if not _NUMERO_IDENTIFICADOR.search(before):
            text = before
    if not re.search(r"[^\W\d_]", text):
        return ""
    text = re.sub(r"[\W_]+", " ", text).strip()
    return EQUIVALENCIAS.get(text, text)[:120].strip()
