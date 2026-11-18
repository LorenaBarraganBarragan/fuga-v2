"""
analytics.py — Esquemas de respuesta para estadísticas y agregados (HU-20, HU-21)
"""

from typing import List

from pydantic import BaseModel


class AnalyticsSummaryResponse(BaseModel):
    periodo: str
    monto_total_cop: int
    cantidad_gastos: int
    promedio_gasto_cop: int


class CategoryBreakdownItemResponse(BaseModel):
    categoria_id: str
    categoria_nombre: str
    monto_cop: int
    cantidad: int
    porcentaje: float


class AnalyticsByCategoryResponse(BaseModel):
    periodo: str
    items: List[CategoryBreakdownItemResponse]
    categorias_mayor_gasto: List[str] = []
