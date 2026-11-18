"""
router.py — Agregador de rutas API v1 para FUGA+
"""

from fastapi import APIRouter

from app.api.v1 import admin, analytics, categories, expenses, health, leaks, me

api_v1_router = APIRouter()

api_v1_router.include_router(health.router)
api_v1_router.include_router(me.router)
api_v1_router.include_router(categories.router)
api_v1_router.include_router(expenses.router)
api_v1_router.include_router(analytics.router)
api_v1_router.include_router(leaks.router)
api_v1_router.include_router(admin.router)
