"""
test_ownership.py — Pruebas de scoping estricto y autorización por propietario (RF-033, F4)
"""

import uuid
import pytest
from app.repositories.base import ScopedRepository
from app.repositories.categories import CategoriesRepository
from app.core.errors import ForbiddenException, ValidationException


def test_scoped_repository_exige_uuid():
    with pytest.raises(ValidationException):
        ScopedRepository(usuario_id=None)

    with pytest.raises(ValidationException):
        ScopedRepository(usuario_id="uuid-invalido")


def test_scoped_repository_asegura_propietario():
    uid_a = uuid.uuid4()
    uid_b = uuid.uuid4()
    repo_a = ScopedRepository(usuario_id=uid_a)

    # El mismo usuario pasa
    repo_a.asegurar_propietario(uid_a)

    # Usuario ajeno lanza ForbiddenException
    with pytest.raises(ForbiddenException):
        repo_a.asegurar_propietario(uid_b)


def test_catalogo_categorias_retorna_9():
    repo = CategoriesRepository()
    cats = repo.list_all()
    assert len(cats) == 9
    assert [c["orden"] for c in cats] == list(range(1, 10))
    nombres = [c["nombre"] for c in cats]
    assert "Alimentación" in nombres
    assert "Transporte" in nombres
    assert "Otros" in nombres
