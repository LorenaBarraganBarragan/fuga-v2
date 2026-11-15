"""
main.py — Aplicación principal FastAPI de FUGA+
"""

from __future__ import annotations

import uuid
from typing import Callable

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.health import router as health_root_router
from app.api.v1.router import api_v1_router
from app.core.config import settings
from app.core.errors import AppException
from app.core.logging import logger, setup_logging

# Inicializar logging
setup_logging(settings.LOG_LEVEL)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    docs_url="/docs" if settings.APP_ENV != "prod" else None,
    redoc_url=None,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def correlation_id_middleware(request: Request, call_next: Callable):
    """Asigna o propaga el Correlation ID en cada solicitud."""
    cid = request.headers.get("X-Correlation-ID") or str(uuid.uuid4())
    request.state.correlation_id = cid

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = cid
    return response


@app.exception_handler(AppException)
async def app_exception_handler(request: Request, exc: AppException):
    cid = getattr(request.state, "correlation_id", str(uuid.uuid4()))
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(correlation_id=cid),
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    cid = getattr(request.state, "correlation_id", str(uuid.uuid4()))
    details = []
    for err in exc.errors():
        field_name = ".".join(str(loc) for loc in err["loc"] if loc != "body")
        details.append({
            "field": field_name or "body",
            "issue": err.get("type", "invalid"),
            "message": err.get("msg", ""),
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Error de validación en los datos proporcionados.",
                "details": details,
                "correlation_id": cid,
            }
        },
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    cid = getattr(request.state, "correlation_id", str(uuid.uuid4()))
    logger.exception("Error no controlado", extra={"correlation_id": cid})
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Ha ocurrido un error interno en el servidor.",
                "details": [],
                "correlation_id": cid,
            }
        },
    )


# Routers
app.include_router(health_root_router)  # /health y /ready en la raíz
app.include_router(api_v1_router, prefix=settings.API_V1_PREFIX)
