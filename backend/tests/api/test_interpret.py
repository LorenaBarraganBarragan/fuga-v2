from app.repositories.categories import CATALOGO_ESTATICO


def test_interpret_http(private_client, monkeypatch):
    monkeypatch.setattr(
        "app.repositories.categories.CategoriesRepository.list_all",
        lambda self, db: CATALOGO_ESTATICO,
    )
    res = private_client.post(
        "/api/v1/expenses/interpret", json={"texto": "Hoy gasté $8.000 en taxi"}
    )
    assert res.status_code == 200
    assert res.json()["draft"]["monto_cop"] == 8000
    assert res.json()["draft"]["categoria_id"] == CATALOGO_ESTATICO[1]["id"]


def test_interpret_requires_auth(client):
    assert client.post("/api/v1/expenses/interpret", json={"texto": "taxi 8000"}).status_code == 401


def test_interpret_validation(private_client):
    assert private_client.post("/api/v1/expenses/interpret", json={"texto": " "}).status_code == 422
