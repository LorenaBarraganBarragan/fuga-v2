"""
categories.py — Repositorio del catálogo cerrado de categorías (D-02)
"""

from typing import List, Optional
from uuid import UUID
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.domain.expenses.diccionario_v1 import CATEGORIAS

# UUIDs canónicos para modo local/offline si la BD no está conectada
CATALOGO_ESTATICO = [
    {
        "id": "10000000-0000-0000-0000-000000000001",
        "nombre": "Alimentación",
        "orden": 1,
        "activa": True,
    },
    {
        "id": "10000000-0000-0000-0000-000000000002",
        "nombre": "Transporte",
        "orden": 2,
        "activa": True,
    },
    {
        "id": "10000000-0000-0000-0000-000000000003",
        "nombre": "Vivienda",
        "orden": 3,
        "activa": True,
    },
    {
        "id": "10000000-0000-0000-0000-000000000004",
        "nombre": "Servicios",
        "orden": 4,
        "activa": True,
    },
    {
        "id": "10000000-0000-0000-0000-000000000005",
        "nombre": "Educación",
        "orden": 5,
        "activa": True,
    },
    {
        "id": "10000000-0000-0000-0000-000000000006",
        "nombre": "Salud",
        "orden": 6,
        "activa": True,
    },
    {
        "id": "10000000-0000-0000-0000-000000000007",
        "nombre": "Entretenimiento",
        "orden": 7,
        "activa": True,
    },
    {
        "id": "10000000-0000-0000-0000-000000000008",
        "nombre": "Compras",
        "orden": 8,
        "activa": True,
    },
    {
        "id": "10000000-0000-0000-0000-000000000009",
        "nombre": "Otros",
        "orden": 9,
        "activa": True,
    },
]


class CategoriesRepository:
    """Acceso al catálogo de categorías."""

    def list_all(self, db: Optional[Session] = None) -> List[dict]:
        if db is not None and isinstance(db, Session):
            try:
                result = db.execute(
                    text("SELECT id, nombre, orden, activa FROM categoria WHERE activa = TRUE ORDER BY orden ASC")
                )
                rows = result.fetchall()
                if rows:
                    return [
                        {"id": str(r[0]), "nombre": r[1], "orden": r[2], "activa": r[3]}
                        for r in rows
                    ]
            except Exception:
                pass

        # Fallback a catálogo canónico estático
        return sorted(CATALOGO_ESTATICO, key=lambda c: c["orden"])

    def get_by_id(self, category_id: UUID, db: Optional[Session] = None) -> Optional[dict]:
        all_cats = self.list_all(db)
        cid_str = str(category_id)
        for cat in all_cats:
            if cat["id"] == cid_str:
                return cat
        return None
