"""
analytics_service.py — Servicio de estadísticas y agregados (HU-20, HU-21)
"""

from typing import Any, Dict, List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.domain.analytics.aggregations import (
    calcular_desglose_categorias,
    calcular_resumen,
)
from app.schemas.analytics import (
    AnalyticsByCategoryResponse,
    AnalyticsSummaryResponse,
    CategoryBreakdownItemResponse,
)


class AnalyticsService:
    @staticmethod
    def get_summary(
        usuario_id: UUID,
        periodo: str,
        db: Optional[Session] = None,
    ) -> AnalyticsSummaryResponse:
        gastos: List[Dict[str, Any]] = []
        if db is not None:
            # Consulta filtrando estrictamente por usuario_id y periodo YYYY-MM
            try:
                res = db.execute(
                    text(
                        "SELECT monto_cop FROM gasto "
                        "WHERE usuario_id = :uid "
                        "AND to_char(fecha_gasto, 'YYYY-MM') = :periodo "
                        "AND deleted_at IS NULL"
                    ),
                    {"uid": str(usuario_id), "periodo": periodo},
                )
                gastos = [{"monto_cop": r[0]} for r in res.fetchall()]
            except Exception:
                pass

        resumen = calcular_resumen(gastos, periodo=periodo)
        return AnalyticsSummaryResponse(
            periodo=resumen.periodo,
            monto_total_cop=resumen.monto_total_cop,
            cantidad_gastos=resumen.cantidad_gastos,
            promedio_gasto_cop=resumen.promedio_gasto_cop,
        )

    @staticmethod
    def get_by_category(
        usuario_id: UUID,
        periodo: str,
        db: Optional[Session] = None,
    ) -> AnalyticsByCategoryResponse:
        gastos: List[Dict[str, Any]] = []
        if db is not None:
            try:
                res = db.execute(
                    text(
                        "SELECT categoria_id, monto_cop FROM gasto "
                        "WHERE usuario_id = :uid "
                        "AND to_char(fecha_gasto, 'YYYY-MM') = :periodo "
                        "AND deleted_at IS NULL"
                    ),
                    {"uid": str(usuario_id), "periodo": periodo},
                )
                gastos = [{"categoria_id": str(r[0]), "monto_cop": r[1]} for r in res.fetchall()]
            except Exception:
                pass

        desglose = calcular_desglose_categorias(gastos, periodo=periodo)
        items = [
            CategoryBreakdownItemResponse(
                categoria_id=d.categoria_id,
                categoria_nombre=d.categoria_nombre,
                monto_cop=d.monto_cop,
                cantidad=d.cantidad,
                porcentaje=d.porcentaje,
            )
            for d in desglose
        ]
        return AnalyticsByCategoryResponse(periodo=periodo, items=items)
