"""HU-08: signed uploads, serialized attachment and conservative asset cleanup."""

import hashlib
import re
import time
from urllib.parse import quote, urlsplit
from uuid import UUID, uuid4

import httpx
from sqlalchemy import text

from app.core.config import settings
from app.core.errors import (
    AppException,
    ForbiddenException,
    NotFoundException,
    RateLimitedException,
    UpstreamException,
)

MAX_BYTES = 5_000_000
UPLOAD_LIFETIME = 3600
CLEANUP_GRACE = 7200  # Cloudinary signatures remain valid for one hour.


def invalid(message="Fotografía no válida.", *, oversized=False):
    return AppException("PHOTO_TOO_LARGE" if oversized else "INVALID_PHOTO", message,
                        status_code=413 if oversized else 400)


def cloud_config():
    if not all((settings.CLOUDINARY_CLOUD_NAME, settings.CLOUDINARY_API_KEY,
                settings.CLOUDINARY_API_SECRET)):
        raise UpstreamException("Fotografías no disponibles: Cloudinary no está configurado.")


def signed(params):
    source = "&".join(f"{key}={params[key]}" for key in sorted(params))
    return hashlib.sha1((source + settings.CLOUDINARY_API_SECRET).encode()).hexdigest()


def owned_id(public_id, user_id):
    return bool(re.fullmatch(r"fuga/" + re.escape(str(user_id)) + r"/[0-9a-f]{32}", public_id))


def lock_profile(db, user_id):
    row = db.execute(text("SELECT foto_url FROM public.perfil WHERE id=:uid FOR UPDATE"),
                     {"uid": str(user_id)}).first()
    if row is None:
        raise NotFoundException("Perfil no encontrado.")
    return row[0]


def load_attempt(db, user_id, public_id):
    if not owned_id(public_id, user_id):
        raise ForbiddenException("No puedes modificar una fotografía ajena o no autorizada.")
    row = db.execute(text("""SELECT estado,secure_url,extract(epoch FROM created_at) AS issued
        FROM public.perfil_foto_carga WHERE public_id=:pid AND usuario_id=:uid FOR UPDATE"""),
                     {"pid": public_id, "uid": str(user_id)}).mappings().first()
    if row is None:
        raise invalid("La carga no pertenece a esta sesión de usuario.")
    return row


def issue_upload(db, user_id):
    cloud_config()
    lock_profile(db, user_id)
    recent = db.execute(text("""SELECT count(*) FROM public.perfil_foto_carga
        WHERE usuario_id=:uid AND created_at>now()-interval '1 hour'"""),
                        {"uid": str(user_id)}).scalar_one()
    if recent >= 10:
        raise RateLimitedException("Demasiados intentos de fotografía. Intenta más tarde.")
    public_id = f"fuga/{user_id}/{uuid4().hex}"
    db.execute(text("""INSERT INTO public.perfil_foto_carga(public_id,usuario_id)
        VALUES (:pid,:uid)"""), {"pid": public_id, "uid": str(user_id)})
    db.commit()  # Register ownership before exposing a usable signature.
    params = {"timestamp": int(time.time()), "public_id": public_id,
              "overwrite": "false", "allowed_formats": "jpg,jpeg,png,webp"}
    return {**params, "signature": signed(params), "api_key": settings.CLOUDINARY_API_KEY,
            "cloud_name": settings.CLOUDINARY_CLOUD_NAME,
            "upload_url": f"https://api.cloudinary.com/v1_1/{settings.CLOUDINARY_CLOUD_NAME}/image/upload"}


def cloud_client():
    return httpx.Client(timeout=10, follow_redirects=False)


def verify_asset(public_id):
    try:
        with cloud_client() as client:
            response = client.get(
                f"https://api.cloudinary.com/v1_1/{settings.CLOUDINARY_CLOUD_NAME}"
                f"/resources/image/upload/{quote(public_id, safe='')}",
                auth=(settings.CLOUDINARY_API_KEY, settings.CLOUDINARY_API_SECRET))
            response.raise_for_status()
            asset = response.json()
    except (httpx.HTTPError, ValueError):
        raise UpstreamException("No se pudo verificar la fotografía. Puedes reintentar.") from None
    if not isinstance(asset, dict):
        raise invalid()
    size = asset.get("bytes")
    if isinstance(size, int) and size > MAX_BYTES:
        raise invalid("La fotografía debe tener máximo 5 MB.", oversized=True)
    if (asset.get("public_id") != public_id or asset.get("resource_type") != "image"
            or asset.get("type") != "upload" or asset.get("format") not in {"jpeg", "jpg", "png", "webp"}
            or not isinstance(size, int) or isinstance(size, bool) or size <= 0
            or not isinstance(asset.get("width"), int) or asset["width"] <= 0
            or not isinstance(asset.get("height"), int) or asset["height"] <= 0):
        raise invalid("Selecciona una imagen JPEG, PNG o WebP válida.")
    url = asset.get("secure_url")
    try:
        parsed = urlsplit(url) if isinstance(url, str) else None
        valid = (parsed and parsed.scheme == "https" and parsed.netloc == "res.cloudinary.com"
                 and parsed.path.startswith(f"/{settings.CLOUDINARY_CLOUD_NAME}/image/upload/")
                 and not parsed.query and not parsed.fragment)
        # The response URL must actually identify the requested asset, not another account's image.
        valid = valid and re.search(r"/(?:v[0-9]+/)?" + re.escape(public_id)
                                    + r"\.(?:jpg|jpeg|png|webp)$", parsed.path)
    except ValueError:
        valid = False
    if not valid:
        raise invalid("URL de imagen no válida.")
    return url


def complete_upload(db, user_id, public_id):
    cloud_config()
    current = lock_profile(db, user_id)
    attempt = load_attempt(db, user_id, public_id)
    if attempt["estado"] == "activa" and current == attempt["secure_url"]:
        db.commit()  # Idempotent retry after a lost response; never reactivates retired uploads.
        return
    if attempt["estado"] != "pendiente" or time.time() - float(attempt["issued"]) > UPLOAD_LIFETIME:
        raise invalid("La carga expiró o fue cancelada. Selecciona nuevamente la fotografía.")
    url = verify_asset(public_id)  # Keep previous URL unchanged on every verification failure.
    db.execute(text("""UPDATE public.perfil_foto_carga SET estado='retirada',updated_at=now()
        WHERE usuario_id=:uid AND estado='activa'"""), {"uid": str(user_id)})
    db.execute(text("""UPDATE public.perfil_foto_carga SET estado='activa',secure_url=:url,
        updated_at=now() WHERE public_id=:pid AND usuario_id=:uid"""),
               {"url": url, "pid": public_id, "uid": str(user_id)})
    db.execute(text("UPDATE public.perfil SET foto_url=:url WHERE id=:uid"),
               {"url": url, "uid": str(user_id)})
    db.commit()


def cancel_upload(db, user_id, public_id):
    lock_profile(db, user_id)
    attempt = load_attempt(db, user_id, public_id)
    state = attempt["estado"]
    if state == "pendiente":
        db.execute(text("""UPDATE public.perfil_foto_carga SET estado='cancelada',updated_at=now()
            WHERE public_id=:pid AND usuario_id=:uid"""), {"pid": public_id, "uid": str(user_id)})
        state = "cancelada"
    db.commit()
    return {"estado": state}  # Active uploads are never undone by a delayed cancel.


def destroy_asset(public_id):
    cloud_config()
    params = {"public_id": public_id, "timestamp": int(time.time()), "invalidate": "true"}
    try:
        with cloud_client() as client:
            response = client.post(
                f"https://api.cloudinary.com/v1_1/{settings.CLOUDINARY_CLOUD_NAME}/image/destroy",
                data={**params, "api_key": settings.CLOUDINARY_API_KEY, "signature": signed(params)})
            response.raise_for_status()
            result = response.json()
        return isinstance(result, dict) and result.get("result") in {"ok", "not found"}
    except (httpx.HTTPError, ValueError):
        return False


def cleanup_uploads(db, *, apply=False, limit=50):
    """Bounded, explicit cleanup. No remote request in dry-run; no arbitrary IDs from a caller."""
    candidates = db.execute(text("""SELECT public_id,usuario_id FROM public.perfil_foto_carga
        WHERE estado IN ('pendiente','retirada','cancelada')
          AND updated_at<now()-make_interval(secs=>:grace)
        ORDER BY updated_at LIMIT :limit"""),
                            {"grace": CLEANUP_GRACE, "limit": min(max(limit, 1), 100)}).all()
    summary = {"candidates": len(candidates), "deleted": 0, "retained": 0, "dry_run": not apply}
    for public_id, user_id in candidates:
        current = lock_profile(db, user_id)
        attempt = load_attempt(db, UUID(str(user_id)), public_id)
        referenced = attempt["secure_url"] and db.execute(text(
            "SELECT 1 FROM public.perfil WHERE foto_url=:url LIMIT 1"),
            {"url": attempt["secure_url"]}).first()
        # Recheck under the same profile/attempt locks used by completion and cancellation.
        eligible = db.execute(text("""SELECT 1 FROM public.perfil_foto_carga WHERE public_id=:pid
            AND estado IN ('pendiente','retirada','cancelada')
            AND updated_at<now()-make_interval(secs=>:grace)"""),
                              {"pid": public_id, "grace": CLEANUP_GRACE}).first()
        if not eligible or referenced or (current and public_id in current):
            summary["retained"] += 1
        elif apply:
            if destroy_asset(public_id):
                db.execute(text("""UPDATE public.perfil_foto_carga SET estado='eliminada',
                    updated_at=now() WHERE public_id=:pid AND usuario_id=:uid"""),
                           {"pid": public_id, "uid": str(user_id)})
                summary["deleted"] += 1
            else:
                summary["retained"] += 1
        db.commit()
    return summary
