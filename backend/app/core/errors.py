"""
errors.py — Jerarquía centralizada de errores (RFC 7807 simplificado) para FUGA+
"""

from __future__ import annotations

from typing import Any, Optional


class AppException(Exception):
    """Excepción base de la aplicación FUGA+."""

    def __init__(
        self,
        code: str,
        message: str,
        status_code: int = 400,
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(message)
        self.code = code
        self.message = message
        self.status_code = status_code
        self.details = details or []

    def to_dict(self, correlation_id: str = "") -> dict[str, Any]:
        return {
            "error": {
                "code": self.code,
                "message": self.message,
                "details": self.details,
                "correlation_id": correlation_id,
            }
        }


class UnauthenticatedException(AppException):
    def __init__(
        self,
        message: str = "Autenticación requerida. Token ausente, inválido o expirado.",
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            code="UNAUTHENTICATED",
            message=message,
            status_code=401,
            details=details,
        )


class AccountDisabledException(AppException):
    def __init__(
        self,
        message: str = "La cuenta se encuentra deshabilitada.",
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            code="ACCOUNT_DISABLED",
            message=message,
            status_code=403,
            details=details,
        )


class ForbiddenException(AppException):
    def __init__(
        self,
        message: str = "No tienes permisos para acceder a este recurso.",
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            code="FORBIDDEN",
            message=message,
            status_code=403,
            details=details,
        )


class NotFoundException(AppException):
    def __init__(
        self,
        message: str = "Recurso no encontrado.",
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            code="NOT_FOUND",
            message=message,
            status_code=404,
            details=details,
        )


class ValidationException(AppException):
    def __init__(
        self,
        message: str = "Error de validación en los datos proporcionados.",
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            code="VALIDATION_ERROR",
            message=message,
            status_code=422,
            details=details,
        )


class IdempotencyConflictException(AppException):
    def __init__(
        self,
        message: str = "Conflicto de idempotencia: misma clave con contenido diferente.",
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            code="IDEMPOTENCY_CONFLICT",
            message=message,
            status_code=409,
            details=details,
        )


class IdempotencyExpiredException(AppException):
    def __init__(
        self,
        message: str = "La clave de idempotencia ha expirado (ventana de 24 horas).",
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            code="IDEMPOTENCY_EXPIRED",
            message=message,
            status_code=409,
            details=details,
        )


class RateLimitedException(AppException):
    def __init__(
        self,
        message: str = "Límite de solicitudes excedido. Intenta más tarde.",
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            code="RATE_LIMITED",
            message=message,
            status_code=429,
            details=details,
        )


class UpstreamException(AppException):
    def __init__(
        self,
        message: str = "Servicio o base de datos no disponible.",
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            code="UPSTREAM_ERROR",
            message=message,
            status_code=503,
            details=details,
        )


class InternalException(AppException):
    def __init__(
        self,
        message: str = "Error interno del servidor.",
        details: Optional[list[dict[str, Any]]] = None,
    ):
        super().__init__(
            code="INTERNAL_ERROR",
            message=message,
            status_code=500,
            details=details,
        )
