"""Perfil propio y carga de imágenes controlada por backend."""

import hashlib
import time
from typing import Literal
from urllib.parse import urlparse
from uuid import uuid4

import httpx
from fastapi import APIRouter, Depends
from pydantic import BaseModel, Field
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.errors import ForbiddenException, UpstreamException, ValidationException
from app.core.security import CurrentUser, get_current_user, get_token_claims, require_user
from app.db.session import get_db
from app.repositories.profiles import ProfilesRepository
from app.schemas.auth import ProfileBootstrapRequest, ProfileResponse, ProfileUpdateRequest

router = APIRouter(prefix="/me", tags=["identity"])


class DeactivateRequest(BaseModel):
    confirmado: Literal[True]


@router.post("/deactivate")
def deactivate(
    body: DeactivateRequest,
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    from app.services.accounts_service import change_state

    return change_state(user.user_id, False, user.user_id, db, allow_self=True)


class GooglePhoto(BaseModel):
    url: str = Field(max_length=2000)


@router.post("/photo/google", response_model=ProfileResponse)
def google_photo(
    body: GooglePhoto,
    claims: dict = Depends(get_token_claims),
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    if "google" not in claims.get("app_metadata", {}).get("providers", []):
        raise ForbiddenException("La cuenta no tiene una identidad Google vinculada.")
    try:
        parsed = urlparse(body.url)
        port = parsed.port
    except ValueError:
        raise ValidationException("Fotografía de Google no válida.") from None
    if (
        parsed.scheme != "https"
        or not (parsed.hostname or "").endswith(".googleusercontent.com")
        or parsed.username
        or parsed.password
        or port not in (None, 443)
    ):
        raise ValidationException("Fotografía de Google no válida.")
    db.execute(
        text("UPDATE perfil SET foto_google_url=:url WHERE id=:uid"),
        {"url": body.url, "uid": str(user.user_id)},
    )
    db.commit()
    return ProfilesRepository(user.user_id).get_profile(db)


@router.get("", response_model=ProfileResponse)
def get_current_user_profile(
    user: CurrentUser = Depends(get_current_user), db: Session = Depends(get_db)
):
    return ProfilesRepository(user.user_id).get_profile(db)


@router.post("/bootstrap", response_model=ProfileResponse)
def bootstrap_profile(
    body: ProfileBootstrapRequest | None = None,
    user: CurrentUser = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return ProfilesRepository(user.user_id).ensure_profile(
        db, body.nombres if body else None, body.apellido if body else None
    )


@router.patch("", response_model=ProfileResponse)
def update_profile(
    body: ProfileUpdateRequest,
    user: CurrentUser = Depends(require_user),
    db: Session = Depends(get_db),
):
    fields = body.model_dump(exclude_unset=True)
    # foto_url is set only by a verified upload, never an arbitrary client URL.
    if "foto_url" in fields:
        raise ValidationException("Utiliza el flujo de carga de fotografía.")
    if fields:
        clauses = ",".join(k + "=:" + k for k in fields)
        db.execute(
            text("UPDATE perfil SET " + clauses + " WHERE id=:uid"),
            {**fields, "uid": str(user.user_id)},
        )
        db.commit()
    return ProfilesRepository(user.user_id).get_profile(db)


def cloud_config():
    if not all(
        (
            settings.CLOUDINARY_CLOUD_NAME,
            settings.CLOUDINARY_API_KEY,
            settings.CLOUDINARY_API_SECRET,
        )
    ):
        raise UpstreamException("Fotografías no disponibles: Cloudinary no está configurado.")


@router.post("/photo/signature")
def photo_signature(user: CurrentUser = Depends(require_user)):
    cloud_config()
    params = {"timestamp": int(time.time()), "public_id": f"fuga/{user.user_id}/{uuid4()}"}
    source = "&".join(f"{k}={params[k]}" for k in sorted(params)) + settings.CLOUDINARY_API_SECRET
    return {
        **params,
        "signature": hashlib.sha1(source.encode()).hexdigest(),
        "api_key": settings.CLOUDINARY_API_KEY,
        "cloud_name": settings.CLOUDINARY_CLOUD_NAME,
        "upload_url": f"https://api.cloudinary.com/v1_1/{settings.CLOUDINARY_CLOUD_NAME}/image/upload",
    }


class PhotoComplete(BaseModel):
    public_id: str = Field(max_length=180)


@router.post("/photo/complete", response_model=ProfileResponse)
def photo_complete(
    body: PhotoComplete, user: CurrentUser = Depends(require_user), db: Session = Depends(get_db)
):
    cloud_config()
    if not body.public_id.startswith(f"fuga/{user.user_id}/") or ".." in body.public_id:
        raise ValidationException("Fotografía no válida.")
    try:
        with httpx.Client(timeout=10) as client:
            response = client.get(
                f"https://api.cloudinary.com/v1_1/{settings.CLOUDINARY_CLOUD_NAME}/resources/image/upload/{body.public_id}",
                auth=(settings.CLOUDINARY_API_KEY, settings.CLOUDINARY_API_SECRET),
            )
            response.raise_for_status()
            asset = response.json()
    except (httpx.HTTPError, ValueError):
        raise UpstreamException("No se pudo verificar la fotografía.") from None
    if (
        asset.get("format") not in {"jpeg", "jpg", "png", "webp"}
        or asset.get("bytes", 5_000_001) > 5_000_000
    ):
        raise ValidationException("La imagen debe ser JPEG, PNG o WebP y tener máximo 5 MB.")
    url = asset.get("secure_url", "")
    if not url.startswith("https://res.cloudinary.com/"):
        raise ValidationException("URL de imagen no válida.")
    db.execute(
        text("UPDATE perfil SET foto_url=:url WHERE id=:uid"),
        {"url": url, "uid": str(user.user_id)},
    )
    db.commit()
    return ProfilesRepository(user.user_id).get_profile(db)
