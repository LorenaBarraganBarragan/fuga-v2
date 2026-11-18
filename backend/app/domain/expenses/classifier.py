"""
classifier.py — Clasificador determinista de categorías para FUGA+

Reglas (RN-INT-06 / RN-INT-07 / D-02):
  - Las reglas del JSON v1 tienen igual precedencia; el orden del catálogo es visual.
  - Coincidencia de frase más larga gana; el empate residual requiere revisión.
  - Empate entre categorías → "Otros" + aviso de revisión manual
  - Sin coincidencia → "Otros"
  - Las 9 categorías son cerradas; nunca se inventa una nueva

El clasificador recibe el catálogo de categorías como parámetro (inyectado
desde el repositorio en producción) o usa el diccionario local en pruebas.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Optional

from app.domain.expenses.diccionario_v1 import CATEGORIAS, GENERICAS
from app.domain.expenses.normalizer import normalizar_descripcion


@dataclass(frozen=True)
class ClasificacionResultado:
    # Nombre de la categoría ganadora
    categoria_nombre: str
    # ID de la BD (None cuando no hay BD disponible, como en pruebas puras)
    categoria_id: Optional[str]
    confianza: str  # "alta" | "media" | "baja"
    avisos: list[str]
    keyword_encontrada: Optional[str]


def _limpiar_texto_para_clasificar(texto: str) -> str:
    """Utiliza el mismo concepto conservador que el intérprete y FUGA-01."""
    return normalizar_descripcion(texto)


def clasificar(
    texto: str,
    catalogo_ids: Optional[dict[str, str]] = None,
) -> ClasificacionResultado:
    """
    Clasifica el texto en una de las 9 categorías de FUGA+.

    Args:
        texto: Texto del gasto (original o normalizado).
        catalogo_ids: Mapa {nombre_categoria: uuid} proveniente de la BD.
                      Si es None, categoria_id será None (modo prueba).

    Returns:
        ClasificacionResultado con categoría, confianza y avisos.

    >>> r = clasificar("Hoy gasté $8.000 en un taxi")
    >>> r.categoria_nombre
    'Transporte'
    >>> r.confianza
    'alta'
    >>> clasificar("Algo random que no clasifica").categoria_nombre
    'Otros'
    """
    texto_limpio = _limpiar_texto_para_clasificar(texto)
    avisos: list[str] = []

    # Buscar coincidencias para cada categoría (excepto "otros")
    # Estructura: {nombre_categoria: (longitud_max_keyword, keyword)}
    matches: dict[str, tuple[int, str]] = {}

    for clave_cat, info in CATEGORIAS.items():
        if clave_cat == "otros":
            continue
        mejor_len = 0
        mejor_kw = ""
        for kw in info["keywords"]:
            kw_norm = normalizar_descripcion(kw)
            if not kw_norm:
                continue
            # Búsqueda de coincidencia completa de palabra
            patron = re.compile(rf"\b{re.escape(kw_norm)}\b")
            if patron.search(texto_limpio):
                if len(kw_norm) > mejor_len:
                    mejor_len = len(kw_norm)
                    mejor_kw = kw

        if mejor_len > 0:
            matches[info["nombre"]] = (mejor_len, mejor_kw)

    # Verificar si el texto contiene términos genéricos
    coincide_generica = False
    for gen in GENERICAS:
        patron_gen = re.compile(rf"\b{re.escape(normalizar_descripcion(gen))}\b")
        if patron_gen.search(texto_limpio):
            coincide_generica = True
            break

    if not matches:
        if coincide_generica:
            avisos.append("Descripción genérica detectada; se asignó 'Otros'.")
        else:
            avisos.append("Sin coincidencia de categoría; se asignó 'Otros'.")
        return _hacer_otros(catalogo_ids, avisos)

    # Coincidencia más larga gana (RN-INT-06 / Anexo C.2)
    max_len = max(longitud for longitud, _ in matches.values())
    ganadores = {cat: kw for cat, (longitud, kw) in matches.items() if longitud == max_len}

    if len(ganadores) == 1:
        nombre_cat, kw = next(iter(ganadores.items()))
        cat_id = catalogo_ids.get(nombre_cat) if catalogo_ids else None
        return ClasificacionResultado(
            categoria_nombre=nombre_cat,
            categoria_id=cat_id,
            confianza="alta",
            avisos=[],
            keyword_encontrada=kw,
        )

    # Múltiples categorías empataron con la misma longitud de keyword: Otros + aviso (RN-INT-06)
    nombres = sorted(ganadores.keys())
    avisos.append(
        f"Texto coincide con varias categorías ({', '.join(nombres)}). "
        "Se asignó 'Otros'; por favor selecciona la categoría correcta."
    )
    return _hacer_otros(catalogo_ids, avisos)


def _hacer_otros(
    catalogo_ids: Optional[dict[str, str]],
    avisos: list[str],
) -> ClasificacionResultado:
    cat_id = catalogo_ids.get("Otros") if catalogo_ids else None
    return ClasificacionResultado(
        categoria_nombre="Otros",
        categoria_id=cat_id,
        confianza="baja",
        avisos=avisos,
        keyword_encontrada=None,
    )
