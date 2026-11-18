"""
aggregations.py — Cálculos analíticos deterministas y agregaciones (HU-20, HU-21, F7)
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import ROUND_HALF_UP, Decimal
from typing import Any

from app.repositories.categories import CATALOGO_ESTATICO


@dataclass(frozen=True)
class ResumenEstadistico:
    periodo: str
    monto_total_cop: int
    cantidad_gastos: int
    promedio_gasto_cop: int


@dataclass(frozen=True)
class DesgloseCategoriaItem:
    categoria_id: str
    categoria_nombre: str
    monto_cop: int
    cantidad: int
    porcentaje: float


def calcular_resumen(
    gastos: list[dict[str, Any]],
    periodo: str,
) -> ResumenEstadistico:
    """
    Calcula total, cantidad y promedio entero en COP.
    Sin números float en la ruta monetaria (RF-020).
    """
    if not gastos:
        return ResumenEstadistico(
            periodo=periodo,
            monto_total_cop=0,
            cantidad_gastos=0,
            promedio_gasto_cop=0,
        )

    total = sum(int(g["monto_cop"]) for g in gastos)
    # SQL may provide weighted category totals; individual expense rows remain supported.
    cantidad = sum(int(g.get("cantidad", 1)) for g in gastos)
    # Redondeo entero estándar del promedio
    promedio = int((Decimal(total) / cantidad).quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    return ResumenEstadistico(
        periodo=periodo,
        monto_total_cop=total,
        cantidad_gastos=cantidad,
        promedio_gasto_cop=promedio,
    )


def calcular_desglose_categorias(
    gastos: list[dict[str, Any]],
    periodo: str,
    catalogo_categorias: list[dict[str, Any]] | None = None,
) -> list[DesgloseCategoriaItem]:
    """
    Calcula el monto, cantidad y porcentaje (1 decimal) por categoría.
    Garantiza que todas las categorías activas aparezcan ordenadas,
    incluyendo 'Otros' con 0 si no tienen gastos (RF-021).
    """
    cats = catalogo_categorias or CATALOGO_ESTATICO
    total_general = sum(int(g["monto_cop"]) for g in gastos)

    # Acumuladores por ID de categoría
    acumulado_monto: dict[str, int] = {str(c["id"]): 0 for c in cats}
    acumulado_cant: dict[str, int] = {str(c["id"]): 0 for c in cats}

    # Mapa ID a info

    for g in gastos:
        cid = str(g["categoria_id"])
        if cid in acumulado_monto:
            acumulado_monto[cid] += int(g["monto_cop"])
            acumulado_cant[cid] += int(g.get("cantidad", 1))
        else:
            # Si no coincide, agrupar bajo Otros
            otros_id = next(
                (str(c["id"]) for c in cats if c["nombre"] == "Otros"),
                "10000000-0000-0000-0000-000000000009",
            )
            acumulado_monto[otros_id] = acumulado_monto.get(otros_id, 0) + int(g["monto_cop"])
            acumulado_cant[otros_id] = acumulado_cant.get(otros_id, 0) + int(g.get("cantidad", 1))

    items: list[DesgloseCategoriaItem] = []
    for c in sorted(cats, key=lambda x: x["orden"]):
        cid = str(c["id"])
        monto = acumulado_monto.get(cid, 0)
        cant = acumulado_cant.get(cid, 0)
        porcentaje = (
            float(
                (Decimal(monto) * 100 / total_general).quantize(
                    Decimal("0.1"), rounding=ROUND_HALF_UP
                )
            )
            if total_general > 0
            else 0.0
        )

        items.append(
            DesgloseCategoriaItem(
                categoria_id=cid,
                categoria_nombre=c["nombre"],
                monto_cop=monto,
                cantidad=cant,
                porcentaje=porcentaje,
            )
        )

    return items
