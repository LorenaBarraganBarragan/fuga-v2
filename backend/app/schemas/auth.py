"""
auth.py — Esquemas de identidad, perfil y sesión de usuario (FUGA+)
"""

from __future__ import annotations

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProfileResponse(BaseModel):
    id: UUID
    nombres: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    foto_url: Optional[str] = None
    rol: str = "usuario"
    disabled_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None


class ProfileBootstrapRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombres: Optional[str] = Field(None, min_length=2, max_length=80)
    apellido: Optional[str] = Field(None, min_length=2, max_length=80)

    @field_validator("nombres", "apellido", mode="before")
    @classmethod
    def recortar_nombre(cls, v):
        return v.strip() if isinstance(v, str) else v


class ProfileUpdateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    nombres: Optional[str] = Field(None, min_length=2, max_length=80)
    apellido: Optional[str] = Field(None, min_length=2, max_length=80)
    telefono: Optional[str] = Field(
        None, pattern=r"^[0-9]{10}$", description="10 dígitos numéricos"
    )
    foto_url: Optional[str] = None

    @field_validator("nombres", "apellido", mode="before")
    @classmethod
    def recortar_nombre(cls, v):
        return v.strip() if isinstance(v, str) else v

    @field_validator("telefono")
    @classmethod
    def validar_telefono(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and (len(v) != 10 or not v.isdigit()):
            raise ValueError("El teléfono debe tener exactamente 10 dígitos numéricos.")
        return v
