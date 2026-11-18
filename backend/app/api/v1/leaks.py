from uuid import UUID

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.security import CurrentUser, require_user
from app.db.session import get_db
from app.schemas.leaks import LeakDetailResponse, LeaksListResponse
from app.services.analytics_service import month_bounds
from app.services.leaks_service import LeaksService

router = APIRouter(prefix="/leaks", tags=["leaks"])


@router.get("", response_model=LeaksListResponse)
def get_leaks(user: CurrentUser = Depends(require_user), db: Session = Depends(get_db)):
    return LeaksService.detect_leaks(user.user_id, db)


@router.get("/monthly-summary")
def monthly_summary(
    periodo: str, user: CurrentUser = Depends(require_user), db: Session = Depends(get_db)
):
    start, end = month_bounds(periodo)
    LeaksService.detect_leaks(user.user_id, db)
    rows = (
        db.execute(
            text("""SELECT DISTINCT g.id,g.monto_cop,f.id AS fuga_id
      FROM fuga f JOIN fuga_evidencia e ON e.fuga_id=f.id JOIN gasto g ON g.id=e.gasto_id
      WHERE f.usuario_id=:uid AND g.usuario_id=:uid AND f.vigente=TRUE
      AND g.deleted_at IS NULL AND g.fecha_gasto>=:start AND g.fecha_gasto<:end"""),
            {"uid": str(user.user_id), "start": start, "end": end},
        )
        .mappings()
        .all()
    )
    amounts = {r["id"]: int(r["monto_cop"]) for r in rows}
    return {
        "periodo": periodo,
        "monto_acumulado_cop": sum(amounts.values()),
        "cantidad_fugas": len({r["fuga_id"] for r in rows}),
        "ocurrencias": len(amounts),
        "mensaje": "Gastos del mes incluidos en posibles fugas vigentes de la ventana actual; no son pérdidas confirmadas.",
    }


@router.get("/{fuga_id}", response_model=LeakDetailResponse)
def get_detail(
    fuga_id: UUID, user: CurrentUser = Depends(require_user), db: Session = Depends(get_db)
):
    return LeaksService.detail(user.user_id, fuga_id, db)
