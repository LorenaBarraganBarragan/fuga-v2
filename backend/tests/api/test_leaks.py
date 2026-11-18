from app.schemas.leaks import LeaksListResponse
from app.services.leaks_service import LeaksService


def test_leaks_http(private_client, monkeypatch):
    monkeypatch.setattr(
        LeaksService,
        "detect_leaks",
        lambda usuario_id, db: LeaksListResponse(
            items=[], total=0, estado="sin_gastos", mensaje_d15="Aún no tienes gastos"
        ),
    )
    res = private_client.get("/api/v1/leaks")
    assert res.status_code == 200
    assert res.json()["estado"] == "sin_gastos"


def test_leaks_requires_auth(client):
    assert client.get("/api/v1/leaks").status_code == 401
