"""
grouping.py — Agrupación de gastos elegibles para detección de fugas (D-01, F8)
"""

from typing import Any, Dict, List, Tuple

from app.domain.expenses.diccionario_v1 import GENERICAS
from app.domain.expenses.normalizer import normalizar_descripcion


def es_descripcion_generica(desc_normalizada: str) -> bool:
    """Verifica si la descripción normalizada coincide con un término genérico."""
    d = desc_normalizada.strip()
    return not d or d in GENERICAS


def agrupar_gastos(
    gastos: List[Dict[str, Any]],
) -> Dict[Tuple[str, str], List[Dict[str, Any]]]:
    """
    Agrupa gastos por (categoria_id, descripcion_normalizada).
    Descarta descripciones genéricas que no deben activar FUGA-01 (F-11).
    """
    grupos: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}

    for g in gastos:
        # Ignorar gastos eliminados lógicamente
        if g.get("deleted_at") is not None:
            continue

        raw_desc = g.get("descripcion", "")
        desc_norm = normalizar_descripcion(raw_desc, int(g["monto_cop"]))

        if es_descripcion_generica(desc_norm):
            continue

        clave = (str(g["categoria_id"]), desc_norm)
        if clave not in grupos:
            grupos[clave] = []
        grupos[clave].append(g)

    return grupos
