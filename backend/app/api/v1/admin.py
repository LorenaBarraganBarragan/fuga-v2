"""Administración: metadatos mínimos, sin acceso a finanzas individuales."""

from uuid import UUID

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.errors import NotFoundException
from app.core.security import CurrentUser, require_admin
from app.db.session import get_db
from app.services.accounts_service import change_state

router = APIRouter(prefix="/admin", tags=["admin"])
BASE = """SELECT p.id,p.nombres,p.apellido,u.email,p.rol,p.disabled_at,p.created_at,
 p.auth_sync_pendiente FROM perfil p JOIN auth.users u ON u.id=p.id"""


def audit(db, actor, action, target=None, result="ok"):
    db.execute(
        text("INSERT INTO auditoria (actor_id,accion,objetivo_id,resultado) VALUES (:a,:b,:c,:d)"),
        {"a": str(actor), "b": action, "c": str(target) if target else None, "d": result},
    )


@router.get("/users")
def users(
    q: str = Query("", max_length=100),
    activo: bool | None = None,
    page: int = Query(1, ge=1),
    limit: int = Query(20, ge=1, le=50),
    user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    where = " WHERE (coalesce(p.nombres,'') ILIKE :q OR coalesce(p.apellido,'') ILIKE :q OR u.email ILIKE :q)"
    params = {
        "q": "%" + q.replace("%", "\\%").replace("_", "\\_") + "%",
        "limit": limit,
        "offset": (page - 1) * limit,
    }
    if activo is not None:
        where += " AND p.disabled_at IS " + ("NULL" if activo else "NOT NULL")
    rows = (
        db.execute(
            text(
                BASE + where + " ORDER BY p.created_at DESC,p.id DESC LIMIT :limit OFFSET :offset"
            ),
            params,
        )
        .mappings()
        .all()
    )
    total = db.execute(
        text("SELECT count(*) FROM perfil p JOIN auth.users u ON u.id=p.id" + where), params
    ).scalar_one()
    audit(db, user.user_id, "consulta_usuarios")
    db.commit()
    return {
        "items": [dict(r) for r in rows],
        "total": total,
        "page": page,
        "has_more": page * limit < total,
    }


@router.get("/users/{uid}")
def detail(uid: UUID, user: CurrentUser = Depends(require_admin), db: Session = Depends(get_db)):
    row = db.execute(text(BASE + " WHERE p.id=:id"), {"id": str(uid)}).mappings().first()
    if not row:
        raise NotFoundException()
    audit(db, user.user_id, "consulta_usuario", uid)
    db.commit()
    return dict(row)


class AccountState(BaseModel):
    activo: bool


@router.patch("/users/{uid}/state")
def state(
    uid: UUID,
    body: AccountState,
    user: CurrentUser = Depends(require_admin),
    db: Session = Depends(get_db),
):
    return change_state(uid, body.activo, user.user_id, db)


@router.get("/stats")
def stats(user: CurrentUser = Depends(require_admin), db: Session = Depends(get_db)):
    counts = (
        db.execute(
            text("""SELECT count(*) AS registrados,
      count(*) FILTER (WHERE disabled_at IS NULL) AS activos,
      count(*) FILTER (WHERE disabled_at IS NOT NULL) AS inactivos FROM perfil""")
        )
        .mappings()
        .one()
    )
    monthly = (
        db.execute(
            text("""SELECT periodo,count(*) AS usuarios_activos
      FROM actividad_mensual GROUP BY periodo ORDER BY periodo DESC LIMIT 12""")
        )
        .mappings()
        .all()
    )
    # No financial aggregates or per-user financial counts are exposed.
    audit(db, user.user_id, "consulta_estadisticas")
    db.commit()
    return {**dict(counts), "actividad_mensual": [dict(r) for r in monthly]}
