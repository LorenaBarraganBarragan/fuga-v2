"""Detección bajo demanda, snapshots versionados y evidencia propia."""

import hashlib
import json
from datetime import datetime, timedelta
from uuid import UUID, uuid4
from zoneinfo import ZoneInfo

from sqlalchemy import text

from app.core.errors import NotFoundException, UpstreamException
from app.domain.expenses.diccionario_v1 import NORMALIZACION_VERSION
from app.domain.expenses.normalizer import normalizar_descripcion
from app.domain.leaks.grouping import es_descripcion_generica
from app.domain.leaks.rule_fuga_01 import evaluar_fuga_01
from app.repositories.expenses import lock_user
from app.schemas.leaks import (
    LeakDetailResponse,
    LeakEvidenceItem,
    LeakItemResponse,
    LeaksListResponse,
)

MESSAGE = (
    "Se identificaron posibles patrones repetidos. "
    "Revisa la evidencia para decidir si representan una fuga de dinero."
)


def empty_state(expenses, parameters):
    if not expenses:
        return "sin_gastos", "Aún no tienes gastos registrados en este periodo."
    eligible = [
        g
        for g in expenses
        if parameters["monto_min"] <= int(g["monto_cop"]) <= parameters["monto_max"]
        and not es_descripcion_generica(
            normalizar_descripcion(g["descripcion"], int(g["monto_cop"]))
        )
    ]
    if (
        len(eligible) < parameters["min_gastos"]
        or len({g["fecha_gasto"] for g in eligible}) < parameters["min_fechas"]
    ):
        return (
            "datos_insuficientes",
            "Aún no hay suficientes registros elegibles para identificar patrones.",
        )
    return (
        "sin_posibles_fugas",
        "No se encontraron posibles fugas con los registros de esta ventana.",
    )


class LeaksService:
    @staticmethod
    def detect_leaks(usuario_id, db):
        lock_user(db, usuario_id)
        today = datetime.now(ZoneInfo("America/Bogota")).date()
        rule = (
            db.execute(
                text("""SELECT v.id,v.version,v.parametros FROM regla_fuga r
          JOIN regla_fuga_version v ON v.regla_id=r.id
          WHERE r.codigo='FUGA-01' AND r.activa=TRUE AND v.vigente_hasta IS NULL""")
            )
            .mappings()
            .first()
        )
        if not rule:
            raise UpstreamException("No hay una versión de FUGA-01 configurada.")
        if rule["version"] != "1.0":
            raise UpstreamException("Esta versión de la regla requiere un motor compatible.")
        start = today - timedelta(days=int(rule["parametros"]["ventana_dias"]) - 1)
        expenses = [
            dict(r)
            for r in db.execute(
                text("""SELECT id,categoria_id,monto_cop,descripcion,fecha_gasto,deleted_at
          FROM gasto WHERE usuario_id=:uid AND deleted_at IS NULL
          AND fecha_gasto BETWEEN :start AND :end
          ORDER BY fecha_gasto,id"""),
                {"uid": str(usuario_id), "start": start, "end": today},
            )
            .mappings()
            .all()
        ]
        candidates = evaluar_fuga_01(
            expenses, parametros=rule["parametros"], fecha_referencia=today
        )
        current_ids = {
            str(value)
            for value in db.execute(
                text("SELECT id FROM fuga WHERE usuario_id=:uid AND vigente=TRUE"),
                {"uid": str(usuario_id)},
            )
            .scalars()
            .all()
        }
        expense_by_id = {str(g["id"]): g for g in expenses}
        prepared = []
        for candidate in candidates:
            evidence = [expense_by_id[gid] for gid in candidate.evidencia_gasto_ids]
            digest = hashlib.sha256(
                json.dumps(
                    {"normalizacion_version": NORMALIZACION_VERSION, "gastos": evidence},
                    sort_keys=True,
                    default=str,
                ).encode()
            ).hexdigest()
            params = {
                "uid": str(usuario_id),
                "rv": str(rule["id"]),
                "cat": candidate.categoria_id,
                "desc": candidate.descripcion_normalizada,
                "hash": digest,
            }
            prior = db.execute(
                text("""SELECT id,vigente FROM fuga WHERE usuario_id=:uid AND regla_version_id=:rv
              AND categoria_id=:cat AND descripcion_normalizada=:desc AND evidencia_hash=:hash
              ORDER BY detectada_en DESC LIMIT 1"""),
                params,
            ).first()
            fid = str(prior[0]) if prior else str(uuid4())
            prepared.append((candidate, params, prior, fid))

        retained_ids = {fid for _, _, _, fid in prepared}
        stale_ids = current_ids - retained_ids
        if stale_ids:
            db.execute(
                text("""UPDATE fuga SET vigente=FALSE,actualizada_en=now()
                  WHERE usuario_id=:uid AND vigente=TRUE AND id=ANY(CAST(:ids AS uuid[]))"""),
                {"uid": str(usuario_id), "ids": sorted(stale_ids)},
            )
        category_ids = sorted({c.categoria_id for c in candidates})
        names = (
            dict(
                db.execute(
                    text("SELECT id,nombre FROM categoria WHERE id=ANY(CAST(:ids AS uuid[]))"),
                    {"ids": category_ids},
                ).all()
            )
            if category_ids
            else {}
        )
        names = {str(key): value for key, value in names.items()}
        items = []
        for candidate, params, prior, fid in prepared:
            if prior:
                if not prior[1]:
                    db.execute(
                        text(
                            "UPDATE fuga SET vigente=TRUE,actualizada_en=now() "
                            "WHERE id=:id AND usuario_id=:uid"
                        ),
                        {"id": fid, "uid": str(usuario_id)},
                    )
            else:
                params.update(
                    id=fid,
                    count=candidate.ocurrencias,
                    amount=candidate.monto_acumulado_cop,
                    start=candidate.fecha_desde,
                    end=candidate.fecha_hasta,
                )
                db.execute(
                    text("""INSERT INTO fuga
                  (id,usuario_id,regla_version_id,categoria_id,descripcion_normalizada,ocurrencias,
                   monto_acumulado_cop,fecha_desde,fecha_hasta,evidencia_hash)
                  VALUES (:id,:uid,:rv,:cat,:desc,:count,:amount,:start,:end,:hash)"""),
                    params,
                )
                db.execute(
                    text("""INSERT INTO fuga_evidencia (fuga_id,gasto_id)
                      SELECT :fid,id FROM gasto WHERE usuario_id=:uid AND deleted_at IS NULL
                      AND id=ANY(CAST(:gids AS uuid[]))"""),
                    {"fid": fid, "gids": candidate.evidencia_gasto_ids, "uid": str(usuario_id)},
                )
            items.append(
                LeakItemResponse(
                    id=UUID(fid),
                    categoria_id=UUID(candidate.categoria_id),
                    categoria_nombre=names[candidate.categoria_id],
                    descripcion_normalizada=candidate.descripcion_normalizada,
                    ocurrencias=candidate.ocurrencias,
                    monto_acumulado_cop=candidate.monto_acumulado_cop,
                    fecha_desde=candidate.fecha_desde,
                    fecha_hasta=candidate.fecha_hasta,
                    regla_codigo="FUGA-01",
                    regla_version=rule["version"],
                )
            )
        db.commit()
        state, message = (
            ("candidatos", MESSAGE) if items else empty_state(expenses, rule["parametros"])
        )
        return LeaksListResponse(items=items, total=len(items), estado=state, mensaje_d15=message)

    @staticmethod
    def detail(usuario_id, fuga_id, db):
        current = LeaksService.detect_leaks(usuario_id, db)
        item = next((i for i in current.items if i.id == fuga_id), None)
        if not item:
            raise NotFoundException("Posible fuga no encontrada o ya no vigente.")
        rows = (
            db.execute(
                text("""SELECT g.id,g.fecha_gasto,g.monto_cop,g.descripcion
          FROM fuga_evidencia e JOIN fuga f ON f.id=e.fuga_id JOIN gasto g ON g.id=e.gasto_id
          WHERE f.id=:id AND f.usuario_id=:uid AND g.usuario_id=:uid
          AND f.vigente=TRUE AND g.deleted_at IS NULL
          ORDER BY g.fecha_gasto,g.id"""),
                {"id": str(fuga_id), "uid": str(usuario_id)},
            )
            .mappings()
            .all()
        )
        return LeakDetailResponse(
            fuga=item,
            evidencias=[LeakEvidenceItem(**dict(r)) for r in rows],
            total_evidencias=len(rows),
        )
