from datetime import datetime, timedelta
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.api.v1.router import api_v1_router
from app.core.errors import AppException
from app.db.session import get_db
from app.main import app_exception_handler
from scripts.qa_android import QaIdentityGate, install_qa_controls

pytestmark = pytest.mark.integration


@pytest.fixture
def qa_client(postgres_engine, request):
    app = FastAPI()
    app.add_exception_handler(AppException, app_exception_handler)
    app.include_router(api_v1_router, prefix="/api/v1")

    def database():
        with Session(postgres_engine) as session:
            yield session

    app.dependency_overrides[get_db] = database
    install_qa_controls(app, postgres_engine, QaIdentityGate(), photos=getattr(request, "param", False))
    with TestClient(app) as client:
        yield client


def test_qa_requires_valid_jwt_and_pins_only_the_first_verified_test_user(
    qa_client, signer, database,
):
    assert qa_client.get("/api/v1/me").status_code == 401
    assert qa_client.get(
        "/api/v1/me", headers={"Authorization": "Bearer invalid"}
    ).status_code == 401
    assert not qa_client.get("/_qa/status").json()["fictitious_account_bound"]
    first, second = uuid4(), uuid4()
    headers = {"Authorization": "Bearer " + signer(
        sub=str(first), email="ignored@local.invalid", app_metadata={"role": "administrador"}
    )}
    profile = qa_client.get("/api/v1/me", headers=headers)
    assert profile.status_code == 200
    assert profile.json()["rol"] == "usuario"
    stored = database.execute(
        text("SELECT email,raw_user_meta_data FROM auth.users WHERE id=:uid"), {"uid": first}
    ).one()
    assert stored == ("qa@local.invalid", {})
    assert qa_client.get(
        "/api/v1/me", headers={"Authorization": "Bearer " + signer(sub=str(second))}
    ).status_code == 403
    assert database.execute(
        text("SELECT count(*) FROM auth.users WHERE id=:uid"), {"uid": second}
    ).scalar_one() == 0
    assert qa_client.post("/api/v1/me/deactivate", headers=headers).status_code == 403
    assert qa_client.get("/api/v1/admin/users", headers=headers).status_code == 403


def test_qa_real_routes_interpret_confirm_dashboard_and_detect_only_local_fixtures(
    qa_client, signer,
):
    headers = {"Authorization": "Bearer " + signer(sub=str(uuid4()))}
    assert qa_client.get("/api/v1/me", headers=headers).status_code == 200
    today = datetime.now(ZoneInfo("America/Bogota")).date()
    for offset in (4, 3, 1, 0):
        draft = qa_client.post(
            "/api/v1/expenses/interpret", headers=headers, json={"texto": "Gasté 5000 en café"}
        )
        assert draft.status_code == 200
        result = draft.json()
        body = {key: result["draft"][key] for key in (
            "monto_cop", "descripcion", "categoria_id", "moneda"
        )}
        body.update(
            fecha_gasto=str(today - timedelta(days=offset)),
            diccionario_version=result["diccionario_version"],
            reglas_version=result["reglas_version"],
        )
        key = str(uuid4())
        response = qa_client.post(
            "/api/v1/expenses", headers={**headers, "Idempotency-Key": key}, json=body
        )
        assert response.status_code == 201
        again = qa_client.post(
            "/api/v1/expenses", headers={**headers, "Idempotency-Key": key}, json=body
        )
        assert again.status_code == 200
        assert again.json()["id"] == response.json()["id"]
    period = today.strftime("%Y-%m")
    summary = qa_client.get("/api/v1/analytics/summary?periodo=" + period, headers=headers)
    expected_count = sum((today - timedelta(days=i)).month == today.month for i in (4, 3, 1, 0))
    assert summary.status_code == 200
    assert summary.json()["monto_total_cop"] == 5000 * expected_count
    leaks = qa_client.get("/api/v1/leaks", headers=headers)
    assert leaks.status_code == 200
    assert leaks.json()["items"][0]["monto_acumulado_cop"] == 20000
    status = qa_client.get("/_qa/status").json()
    assert status["expense_count"] == 4
    assert status["total_cop"] == 20000
    assert status["current_leaks"] == 1
    assert "sub" not in status and "email" not in status


@pytest.mark.parametrize("qa_client", [True], indirect=True)
def test_photo_qa_opens_only_owned_upload_routes_and_keeps_other_boundaries(
    qa_client, signer, monkeypatch,
):
    from app.core.config import settings

    monkeypatch.setattr(settings, "CLOUDINARY_API_SECRET", None)
    headers = {"Authorization": "Bearer " + signer(sub=str(uuid4()))}
    assert qa_client.post("/api/v1/me/photo/signature").status_code == 401
    assert qa_client.post("/api/v1/me/photo/signature", headers=headers).status_code == 503
    assert qa_client.post("/api/v1/me/photo/google", headers=headers).status_code == 403
    assert qa_client.post("/api/v1/me/deactivate", headers=headers).status_code == 403
    assert qa_client.get("/api/v1/admin/users", headers=headers).status_code == 403
    assert qa_client.get("/_qa/status").json()["photo_routes_enabled"] is True
