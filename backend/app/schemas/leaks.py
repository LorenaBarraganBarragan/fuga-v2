"""
leaks.py — Esquemas de respuesta para posibles fugas y evidencia (HU-23, HU-24)
"""

from datetime import date
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class LeakItemResponse(BaseModel):
    id: UUID
    categoria_id: UUID
    categoria_nombre: Optional[str] = None
    descripcion_normalizada: str
    ocurrencias: int
    monto_acumulado_cop: int
    fecha_desde: date
    fecha_hasta: date
    regla_codigo: str = "FUGA-01"
    regla_version: str = "1.0"


class LeakEvidenceItem(BaseModel):
    id: UUID
    fecha_gasto: date
    monto_cop: int
    descripcion: str


class LeakDetailResponse(BaseModel):
    fuga: LeakItemResponse
    evidencias: List[LeakEvidenceItem]
    total_evidencias: int


class LeaksListResponse(BaseModel):
    items: List[LeakItemResponse]
    total: int
    estado: str  # sin_gastos | datos_insuficientes | sin_posibles_fugas | candidatos
    mensaje_d15: str
