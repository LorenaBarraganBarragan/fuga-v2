"""
normalizer.py — Normalización de texto para FUGA+

Reglas (RN-INT-01):
  - Convertir a minúsculas
  - Eliminar tildes/diacríticos
  - Colapsar espacios múltiples
  - Eliminar signos redundantes al inicio/final
"""

import unicodedata
import re


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


def normalizar_descripcion(raw: str) -> str:
    """
    Normaliza una descripción de gasto:
    - Aplica normalizar()
    - Trunca a 120 caracteres si es necesario

    >>> normalizar_descripcion("TAXI al Trabajo")
    'taxi al trabajo'
    """
    return normalizar(raw)[:120]
