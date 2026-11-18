"""Consultas por mes con límites explícitos y cálculos exactos."""

import re
from datetime import date, datetime
from decimal import ROUND_HALF_UP, Decimal
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy import text

from app.core.errors import ValidationException
from app.domain.analytics.aggregations import calcular_desglose_categorias, calcular_resumen
from app.repositories.categories import CategoriesRepository
from app.schemas.analytics import (
    AnalyticsByCategoryResponse,
    AnalyticsSummaryResponse,
    CategoryBreakdownItemResponse,
)


def month_bounds(periodo):
    if not re.fullmatch(r"\d{4}-\d{2}", periodo):
        raise ValidationException("Periodo inválido; utiliza YYYY-MM.")
    try:
        first = date.fromisoformat(periodo + "-01")
    except ValueError:
        raise ValidationException("Mes inválido.") from None
    current = datetime.now(ZoneInfo("America/Bogota")).date().replace(day=1)
    if first < date(2020, 1, 1) or first > current:
        raise ValidationException("Selecciona un mes entre enero de 2020 y el actual.")
    end = date(first.year + (first.month == 12), 1 if first.month == 12 else first.month + 1, 1)
    return first, end


class AnalyticsService:
    @staticmethod
    def rows(usuario_id, periodo, db):
        start, end = month_bounds(periodo)
        return [
            dict(r)
            for r in db.execute(
                text("""SELECT categoria_id,SUM(monto_cop) AS monto_cop,COUNT(*) AS cantidad
          FROM gasto
          WHERE usuario_id=:uid AND fecha_gasto>=:start AND fecha_gasto<:end AND deleted_at IS NULL
          GROUP BY categoria_id"""),
                {"uid": str(usuario_id), "start": start, "end": end},
            )
            .mappings()
            .all()
        ]

    @staticmethod
    def get_summary(usuario_id: UUID, periodo: str, db):
        result = calcular_resumen(AnalyticsService.rows(usuario_id, periodo, db), periodo)
        return AnalyticsSummaryResponse(**vars(result))

    @staticmethod
    def get_by_category(usuario_id: UUID, periodo: str, db):
        items = calcular_desglose_categorias(
            AnalyticsService.rows(usuario_id, periodo, db),
            periodo,
            CategoriesRepository().list_all(db),
        )
        maximum = max((x.monto_cop for x in items), default=0)
        names = sorted(x.categoria_nombre for x in items if maximum > 0 and x.monto_cop == maximum)
        return AnalyticsByCategoryResponse(
            periodo=periodo,
            items=[CategoryBreakdownItemResponse(**vars(x)) for x in items],
            categorias_mayor_gasto=names,
        )

    @staticmethod
    def compare(usuario_id, periodo, db):
        selected, _ = month_bounds(periodo)
        previous = date(
            selected.year - (selected.month == 1),
            12 if selected.month == 1 else selected.month - 1,
            1,
        )
        now = AnalyticsService.get_summary(usuario_id, periodo, db)
        if previous < date(2020, 1, 1):
            return {
                "actual": now,
                "anterior": None,
                "diferencia_cop": None,
                "variacion_porcentaje": None,
                "mensaje": "sin base de comparación",
            }
        before = AnalyticsService.get_summary(usuario_id, previous.strftime("%Y-%m"), db)
        difference = now.monto_total_cop - before.monto_total_cop
        variation = (
            float(
                (Decimal(difference) * 100 / before.monto_total_cop).quantize(
                    Decimal("0.1"), rounding=ROUND_HALF_UP
                )
            )
            if before.monto_total_cop
            else None
        )
        return {
            "actual": now,
            "anterior": before,
            "diferencia_cop": difference,
            "variacion_porcentaje": variation,
            "mensaje": "sin base de comparación" if variation is None else None,
        }
