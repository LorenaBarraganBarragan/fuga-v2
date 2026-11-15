"""
leaks_service.py — Servicio de detección bajo demanda y snapshot de fugas (HU-23, HU-24, D-01, D-15)
"""

from datetime import datetime, date, timedelta
from typing import Any, Dict, List, Optional
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.domain.leaks.rule_fuga_01 import FugaCandidata, evaluar_fuga_01
from app.repositories.categories import CategoriesRepository
from app.schemas.leaks import (
    LeakDetailResponse,
    LeakEvidenceItem,
    LeakItemResponse,
    LeaksListResponse,
)

ZONA_BOGOTA = ZoneInfo("America/Bogota")

MENSAJE_SIN_GASTOS = "Aún no tienes gastos registrados en este periodo."
MENSAJE_DATOS_INSUFICIENTES = (
    "Aún no hay suficientes registros en los últimos 30 días para identificar posibles patrones."
)
MENSAJE_CANDIDATOS = (
    "Se identificaron posibles patrones repetidos con base en los gastos que confirmaste. "
    "Revisa la evidencia para decidir si representan una fuga de dinero."
)


class LeaksService:
    @staticmethod
    def detect_leaks(
        usuario_id: UUID,
        db: Optional[Session] = None,
    ) -> LeaksListResponse:
        hoy = datetime.now(tz=ZONA_BOGOTA).date()
        hace_30_dias = hoy - timedelta(days=30)

        gastos: List[Dict[str, Any]] = []
        if db is not None:
            try:
                res = db.execute(
                    text(
                        "SELECT id, categoria_id, monto_cop, descripcion, fecha_gasto, deleted_at "
                        "FROM gasto "
                        "WHERE usuario_id = :uid "
                        "AND fecha_gasto >= :hace_30 "
                        "AND deleted_at IS NULL"
                    ),
                    {"uid": str(usuario_id), "hace_30": hace_30_dias},
                )
                for r in res.fetchall():
                    gastos.append({
                        "id": str(r[0]),
                        "categoria_id": str(r[1]),
                        "monto_cop": r[2],
                        "descripcion": r[3],
                        "fecha_gasto": r[4],
                        "deleted_at": r[5],
                    })
            except Exception:
                pass

        if not gastos:
            return LeaksListResponse(
                items=[],
                total=0,
                estado="sin_gastos",
                mensaje_d15=MENSAJE_SIN_GASTOS,
            )

        candidatas = evaluar_fuga_01(gastos, fecha_referencia=hoy)

        cats_repo = CategoriesRepository()
        mapa_cats = {c["id"]: c["nombre"] for c in cats_repo.list_all(db)}

        if not candidatas:
            return LeaksListResponse(
                items=[],
                total=0,
                estado="datos_insuficientes",
                mensaje_d15=MENSAJE_DATOS_INSUFICIENTES,
            )

        items_resp = []
        for c in candidatas:
            items_resp.append(
                LeakItemResponse(
                    id=uuid4(),
                    categoria_id=UUID(c.categoria_id),
                    categoria_nombre=mapa_cats.get(c.categoria_id, "Desconocida"),
                    descripcion_normalizada=c.descripcion_normalizada,
                    ocurrencias=c.ocurrencias,
                    monto_acumulado_cop=c.monto_acumulado_cop,
                    fecha_desde=c.fecha_desde,
                    fecha_hasta=c.fecha_hasta,
                    regla_codigo=c.regla_codigo,
                    regla_version=c.regla_version,
                )
            )

        return LeaksListResponse(
            items=items_resp,
            total=len(items_resp),
            estado="candidatos",
            mensaje_d15=MENSAJE_CANDIDATOS,
        )
