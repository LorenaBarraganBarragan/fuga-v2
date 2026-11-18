"""
logging.py — Configuración de logging seguro para FUGA+ (RNF-007)
Filtra estrictamente claves sensibles: password, token, authorization, monto_cop, secret, etc.
"""

from __future__ import annotations

import logging
import re
from typing import Any

CLAVES_SENSIBLES = {
    "password",
    "contrasena",
    "contraseña",
    "token",
    "access_token",
    "refresh_token",
    "authorization",
    "monto_cop",
    "monto",
    "secret",
    "service_role",
    "api_key",
    "cloudinary_api_key",
    "cloudinary_api_secret",
    "signature",
    "apikey",
    "supabase_service_role_key",
    "jwt",
    "email",
    "telefono",
    "descripcion",
    "texto",
    "texto_original",
}


def sanitizar_datos(dato: Any) -> Any:
    """
    Sanitiza recursivamente diccionarios o listas eliminando o enmascarando
    claves sensibles antes de escribir a los logs.
    """
    if isinstance(dato, dict):
        sanitizado = {}
        for k, v in dato.items():
            if str(k).lower() in CLAVES_SENSIBLES:
                sanitizado[k] = "[REDACTED]"
            else:
                sanitizado[k] = sanitizar_datos(v)
        return sanitizado
    elif isinstance(dato, (list, tuple)):
        return [sanitizar_datos(item) for item in dato]
    elif isinstance(dato, str):
        # Enmascarar tokens JWT (formato header.payload.signature)
        if re.search(r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+", dato):
            dato = re.sub(
                r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
                "[REDACTED_JWT]",
                dato,
            )
        return re.sub(r"sb_secret_[A-Za-z0-9_-]+", "[REDACTED_SECRET]", dato)
    return dato


class SensitiveFilter(logging.Filter):
    """Filtro de logging para eliminar valores sensibles de los mensajes."""

    def filter(self, record: logging.LogRecord) -> bool:
        if (
            record.name == "uvicorn.access"
            and isinstance(record.args, tuple)
            and len(record.args) == 5
        ):
            values = list(record.args)
            values[2] = str(values[2]).split("?", 1)[0]
            record.args = tuple(values)
        # Includes extra fields attached by log callers. Never render exception SQL/parameters.
        for name, value in list(record.__dict__.items()):
            if name.lower() in CLAVES_SENSIBLES:
                record.__dict__[name] = "[REDACTED]"
            elif isinstance(value, str | dict | list | tuple) and name not in {"args", "exc_info"}:
                record.__dict__[name] = sanitizar_datos(value)
        if record.args:
            if isinstance(record.args, dict):
                record.args = sanitizar_datos(record.args)
            elif isinstance(record.args, (list, tuple)):
                record.args = tuple(sanitizar_datos(a) for a in record.args)
        if record.exc_info:
            record.exc_info = None
            record.exc_text = None
        return True


def setup_logging(level: str = "INFO") -> None:
    """Configura el logger raíz con el filtro de datos sensibles."""
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    logger = logging.getLogger()
    logger.setLevel(numeric_level)

    # Remover handlers existentes si los hay
    for handler in list(logger.handlers):
        logger.removeHandler(handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(numeric_level)
    formatter = logging.Formatter(
        fmt="%(asctime)s [%(levelname)s] [%(name)s] [cid:%(correlation_id)s] %(message)s",
        defaults={"correlation_id": "-"},
    )
    console_handler.setFormatter(formatter)
    console_handler.addFilter(SensitiveFilter())
    logger.addHandler(console_handler)
    # Uvicorn may have non-propagating handlers of its own.
    for name in ("uvicorn.access", "uvicorn.error"):
        target = logging.getLogger(name)
        if not any(isinstance(item, SensitiveFilter) for item in target.filters):
            target.addFilter(SensitiveFilter())


logger = logging.getLogger("fuga_plus")
