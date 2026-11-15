"""
base.py — Clase base para repositorios privados con scoping estricto por usuario_id (RF-033)
"""

from uuid import UUID
from app.core.errors import ForbiddenException, ValidationException


class ScopedRepository:
    """
    Garantiza que toda operación de lectura o mutación en tablas privadas
    exija y aplique el identificador de usuario propietario (usuario_id).
    """

    def __init__(self, usuario_id: UUID):
        if not usuario_id:
            raise ValidationException("Se requiere un usuario_id válido para inicializar el repositorio.")
        if not isinstance(usuario_id, UUID):
            try:
                usuario_id = UUID(str(usuario_id))
            except (ValueError, TypeError):
                raise ValidationException("El usuario_id no tiene formato UUID válido.")
        self.usuario_id = usuario_id

    def asegurar_propietario(self, target_usuario_id: UUID) -> None:
        """Verifica que el usuario_id destino coincida con el usuario propietario."""
        if str(target_usuario_id) != str(self.usuario_id):
            raise ForbiddenException("Acceso denegado: no tienes permisos sobre este recurso.")
