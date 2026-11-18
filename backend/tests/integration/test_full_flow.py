from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from uuid import uuid4
from zoneinfo import ZoneInfo

import pytest
from sqlalchemy import text

pytestmark = pytest.mark.integration


def identity(database, signer, role="usuario"):
    uid = uuid4()
    database.execute(
        text("INSERT INTO auth.users(id,email) VALUES (:id,:email)"),
        {"id": uid, "email": str(uid) + "@test.invalid"},
    )
    database.execute(text("UPDATE perfil SET rol=:role WHERE id=:id"), {"role": role, "id": uid})
    database.commit()
    return uid, {"Authorization": "Bearer " + signer(sub=str(uid))}


def test_full_expense_leak_and_ownership(integrated_client, database, signer):
    client = integrated_client
    uid, headers = identity(database, signer)
    other, other_headers = identity(database, signer)
    admin, admin_headers = identity(database, signer, "administrador")
    assert client.get("/api/v1/me", headers=headers).json()["id"] == str(uid)
    interpreted = client.post(
        "/api/v1/expenses/interpret", headers=headers, json={"texto": "Hoy gasté $8.000 en taxi"}
    )
    assert interpreted.status_code == 200, interpreted.text
    category = interpreted.json()["draft"]["categoria_id"]
    assert category
    today = datetime.now(ZoneInfo("America/Bogota")).date()
    expenses = []
    for i in range(3):
        body = {
            "monto_cop": 8000,
            "descripcion": "taxi",
            "fecha_gasto": str(today - timedelta(days=i)),
            "categoria_id": category,
        }
        result = client.post(
            "/api/v1/expenses", headers={**headers, "Idempotency-Key": str(uuid4())}, json=body
        )
        assert result.status_code == 201, result.text
        assert result.json()["texto_original"] is None
        expenses.append(result.json())
    listed = client.get("/api/v1/expenses?limit=2", headers=headers)
    assert listed.status_code == 200, listed.text
    assert listed.json()["has_more"]
    assert (
        len(
            client.get(
                "/api/v1/expenses", params={"cursor": listed.json()["next_cursor"]}, headers=headers
            ).json()["items"]
        )
        == 1
    )
    assert (
        client.get("/api/v1/expenses/" + expenses[0]["id"], headers=other_headers).status_code
        == 404
    )
    assert client.get("/api/v1/expenses", headers=admin_headers).status_code == 403
    assert client.get("/api/v1/admin/users", headers=headers).status_code == 403
    leaks = client.get("/api/v1/leaks", headers=headers)
    assert leaks.status_code == 200, leaks.text
    assert leaks.json()["total"] == 1
    fid = leaks.json()["items"][0]["id"]
    assert client.get("/api/v1/leaks", headers=headers).json()["items"][0]["id"] == fid
    detail = client.get("/api/v1/leaks/" + fid, headers=headers)
    assert detail.status_code == 200, detail.text
    assert sum(x["monto_cop"] for x in detail.json()["evidencias"]) == 24000
    assert client.get("/api/v1/leaks/" + fid, headers=other_headers).status_code == 404
    summary = client.get("/api/v1/analytics/summary", headers=headers)
    assert summary.json()["monto_total_cop"] == 24000
    breakdown = client.get("/api/v1/analytics/by-category", headers=headers).json()
    assert breakdown["categorias_mayor_gasto"] == ["Transporte"]
    edit = {**body, "monto_cop": 50000}
    assert (
        client.put("/api/v1/expenses/" + expenses[0]["id"], headers=headers, json=edit).status_code
        == 200
    )
    assert client.get("/api/v1/leaks", headers=headers).json()["total"] == 0
    assert client.get("/api/v1/leaks/" + fid, headers=headers).status_code == 404
    assert (
        client.delete("/api/v1/expenses/" + expenses[0]["id"], headers=other_headers).status_code
        == 404
    )
    assert (
        client.delete("/api/v1/expenses/" + expenses[0]["id"], headers=headers).status_code == 204
    )
    assert (
        client.get("/api/v1/analytics/summary", headers=headers).json()["monto_total_cop"] == 16000
    )
    database.execute(text("UPDATE perfil SET disabled_at=now() WHERE id=:id"), {"id": uid})
    database.commit()
    assert client.get("/api/v1/me", headers=headers).status_code == 403


def test_concurrent_idempotency(integrated_client, database, signer):
    uid, headers = identity(database, signer)
    category = integrated_client.get("/api/v1/categories", headers=headers).json()[0]["id"]
    body = {
        "monto_cop": 8000,
        "descripcion": "cafe",
        "fecha_gasto": str(datetime.now(ZoneInfo("America/Bogota")).date()),
        "categoria_id": category,
    }
    headers = {**headers, "Idempotency-Key": str(uuid4())}
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(
            pool.map(
                lambda _: integrated_client.post("/api/v1/expenses", headers=headers, json=body),
                range(2),
            )
        )
    assert sorted(r.status_code for r in results) == [200, 201], [r.text for r in results]
    assert results[0].json()["id"] == results[1].json()["id"]
    conflict = integrated_client.post(
        "/api/v1/expenses", headers=headers, json={**body, "monto_cop": 9000}
    )
    assert conflict.status_code == 409


def test_profile_update_and_admin_metadata(integrated_client, database, signer):
    uid, headers = identity(database, signer)
    aid, admin_headers = identity(database, signer, "administrador")
    res = integrated_client.patch(
        "/api/v1/me", headers=headers, json={"nombres": " Lorena ", "telefono": "3001234567"}
    )
    assert res.status_code == 200, res.text
    assert res.json()["nombres"] == "Lorena"
    assert (
        integrated_client.patch("/api/v1/me", headers=headers, json={"nombres": "a"}).status_code
        == 422
    )
    assert (
        integrated_client.patch(
            "/api/v1/me", headers=headers, json={"foto_url": "https://evil.invalid/a"}
        ).status_code
        == 422
    )
    listed = integrated_client.get("/api/v1/admin/users", headers=admin_headers)
    assert listed.status_code == 200, listed.text
    assert not any(
        "monto" in field or "password" in field for row in listed.json()["items"] for field in row
    )
    stats = integrated_client.get("/api/v1/admin/stats", headers=admin_headers)
    assert stats.status_code == 200, stats.text
    assert (
        database.execute(
            text("SELECT count(*) FROM auditoria WHERE actor_id=:id"), {"id": aid}
        ).scalar_one()
        >= 2
    )


def test_rls_blocks_direct_access(database):
    uid = uuid4()
    database.execute(
        text("INSERT INTO auth.users(id,email) VALUES (:id,'rls@test.invalid')"), {"id": uid}
    )
    database.commit()
    database.execute(text("SET LOCAL ROLE authenticated"))
    database.execute(
        text("SELECT set_config('request.jwt.claims',:claims,true)"),
        {"claims": '{"sub":"' + str(uid) + '"}'},
    )
    assert database.execute(text("SELECT count(*) FROM gasto")).scalar_one() == 0
    with pytest.raises(Exception):
        database.execute(text("UPDATE perfil SET rol='administrador' WHERE id=:id"), {"id": uid})
    database.rollback()
