"""
expenses.py — Esquemas Pydantic para gastos e interpretación (FUGA+)
"""

from __future__ import annotations

from datetime import date, datetime
from typing import Optional
from uuid import UUID
from zoneinfo import ZoneInfo

from pydantic import BaseModel, Field, field_validator

ZONA_BOGOTA = ZoneInfo("America/Bogota")
FECHA_MINIMA = date(2020, 1, 1)


# --- Interpretación (F5) ---


class InterpretRequest(BaseModel):
    texto: str = Field(
        ...,
        min_length=1,
        max_length=280,
        description="Texto libre del gasto escrito por el usuario (máx 280 caracteres)",
    )

    @field_validator("texto")
    @classmethod
    def validar_no_vacio(cls, v: str) -> str:
        s = v.strip()
        if not s:
            raise ValueError("El texto no puede estar vacío.")
        return v


class DraftResponse(BaseModel):
    texto: str
    monto_cop: Optional[int] = Field(None, description="Monto entero en COP o None si no se detectó")
    fecha_gasto: date
    descripcion: str = Field(..., max_length=120)
    categoria_id: Optional[str] = None
    categoria_nombre: str
    moneda: str = "COP"


class InterpretResponse(BaseModel):
    draft: DraftResponse
    confianza: dict[str, str] = Field(
        ...,
        description="Nivel de confianza por campo: 'alta', 'media', 'baja', 'invalido'",
    )
    avisos: list[str] = Field(default_factory=list)
    ambiguedades: list[str] = Field(default_factory=list)
    diccionario_version: str
    reglas_version: str


# --- Creación y Consulta de Gastos (F6) ---


class ExpenseCreate(BaseModel):
    monto_cop: int = Field(..., ge=1, le=100_000_000, description="Monto entero en COP")
    descripcion: str = Field(..., min_length=1, max_length=120, description="Descripción del gasto")
    fecha_gasto: date = Field(..., description="Fecha de realización del gasto")
    categoria_id: UUID = Field(..., description="UUID de la categoría en BD")
    moneda: str = Field("COP", pattern="^COP$", description="Moneda, únicamente 'COP'")
    texto_original: Optional[str] = Field(None, max_length=280)
    diccionario_version: str = Field("1.0", max_length=10)
    reglas_version: str = Field("1.0", max_length=10)

    @field_validator("descripcion")
    @classmethod
    def validar_descripcion(cls, v: str) -> str:
        s = v.strip()
        if len(s) < 1 or len(s) > 120:
            raise ValueError("La descripción debe tener entre 1 y 120 caracteres tras recortar espacios.")
        return s

    @field_validator("fecha_gasto")
    @classmethod
    def validar_fecha_no_futura_y_minima(cls, v: date) -> date:
        if v < FECHA_MINIMA:
            raise ValueError(f"La fecha de gasto no puede ser anterior a {FECHA_MINIMA}.")
        hoy_bogota = datetime.now(tz=ZONA_BOGOTA).date()
        if v > hoy_bogota:
            raise ValueError(
                f"La fecha de gasto ({v}) no puede ser futura respecto a hoy ({hoy_bogota}) en America/Bogota."
            )
        return v


class ExpenseResponse(BaseModel):
    id: UUID
    usuario_id: UUID
    categoria_id: UUID
    categoria_nombre: Optional[str] = None
    monto_cop: int
    descripcion: str
    texto_original: Optional[str] = None
    fecha_gasto: date
    moneda: str
    diccionario_version: str
    reglas_version: str
    clave_idempotencia: UUID
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None


class ExpenseListResponse(BaseModel):
    items: list[ExpenseResponse]
    next_cursor: Optional[str] = None
    has_more: bool
