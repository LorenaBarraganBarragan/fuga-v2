"""
rule_fuga_01.py — Implementación determinista de la regla FUGA-01 v1.0 (D-01, D-15, F8)
Detecta gastos repetidos de bajo monto en una ventana de 30 días con evidencia verificable.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from typing import Any, Dict, List, Optional
from zoneinfo import ZoneInfo

from app.domain.leaks.grouping import agrupar_gastos

PARAMETROS_DEFAULT_V1_0 = {
    "ventana_dias": 30,
    "min_gastos": 3,
    "min_fechas": 3,
    "monto_min": 1000,
    "monto_max": 30000,
    "suma_min": 15000,
    "zona": "America/Bogota",
}


@dataclass(frozen=True)
class FugaCandidata:
    categoria_id: str
    descripcion_normalizada: str
    ocurrencias: int
    monto_acumulado_cop: int
    fecha_desde: date
    fecha_hasta: date
    evidencia_gasto_ids: List[str]
    regla_codigo: str = "FUGA-01"
    regla_version: str = "1.0"


def evaluar_fuga_01(
    gastos: List[Dict[str, Any]],
    parametros: Optional[Dict[str, Any]] = None,
    fecha_referencia: Optional[date] = None,
) -> List[FugaCandidata]:
    """
    Evalúa la regla FUGA-01 v1.0 sobre un conjunto de gastos.

    Criterios de activación (D-01):
      - Ventana de tiempo: fecha_referencia - ventana_dias (30 días)
      - Rango de monto por gasto: entre monto_min (1.000) y monto_max (30.000) COP
      - Cantidad mínima de gastos: min_gastos (3)
      - Fechas distintas mínimas: min_fechas (3)
      - Suma acumulada mínima: suma_min (15.000) COP
    """
    params = {**PARAMETROS_DEFAULT_V1_0, **(parametros or {})}
    ventana_dias = int(params["ventana_dias"])
    min_gastos = int(params["min_gastos"])
    min_fechas = int(params["min_fechas"])
    monto_min = int(params["monto_min"])
    monto_max = int(params["monto_max"])
    suma_min = int(params["suma_min"])

    if fecha_referencia is None:
        from datetime import datetime
        zona = ZoneInfo(params.get("zona", "America/Bogota"))
        fecha_referencia = datetime.now(tz=zona).date()

    fecha_limite_inferior = fecha_referencia - timedelta(days=ventana_dias)

    # 1. Filtrar gastos elegibles para la regla
    elegibles: List[Dict[str, Any]] = []
    for g in gastos:
        # Excluir eliminados
        if g.get("deleted_at") is not None:
            continue

        monto = int(g["monto_cop"])
        if not (monto_min <= monto <= monto_max):
            continue

        fg = g["fecha_gasto"]
        if isinstance(fg, str):
            fg = date.fromisoformat(fg)

        if not (fecha_limite_inferior <= fg <= fecha_referencia):
            continue

        # Copiar y asegurar fecha normalizada
        item = dict(g)
        item["fecha_gasto"] = fg
        elegibles.append(item)

    # 2. Agrupar por categoría y descripción normalizada
    grupos = agrupar_gastos(elegibles)

    # 3. Evaluar umbrales por cada grupo
    candidatas: List[FugaCandidata] = []

    for (cat_id, desc_norm), lista_gastos in grupos.items():
        ocurrencias = len(lista_gastos)
        if ocurrencias < min_gastos:
            continue

        fechas_distintas = {g["fecha_gasto"] for g in lista_gastos}
        if len(fechas_distintas) < min_fechas:
            continue

        suma_acumulada = sum(int(g["monto_cop"]) for g in lista_gastos)
        if suma_acumulada < suma_min:
            continue

        fechas_ordenadas = sorted(fechas_distintas)
        evidencia_ids = [str(g["id"]) for g in lista_gastos]

        candidatas.append(
            FugaCandidata(
                categoria_id=cat_id,
                descripcion_normalizada=desc_norm,
                ocurrencias=ocurrencias,
                monto_acumulado_cop=suma_acumulada,
                fecha_desde=fechas_ordenadas[0],
                fecha_hasta=fechas_ordenadas[-1],
                evidencia_gasto_ids=evidencia_ids,
                regla_codigo="FUGA-01",
                regla_version="1.0",
            )
        )

    return candidatas
