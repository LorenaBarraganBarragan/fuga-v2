import pytest
import asyncio
import pytest_asyncio
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient
from app.main import app
import os

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest_asyncio.fixture(scope="session")
async def test_db():
    mongo_uri = os.getenv("TEST_MONGODB_URI")
    if not mongo_uri:
        pytest.skip("TEST_MONGODB_URI not set")
    test_db_name = os.getenv("TEST_MONGODB_DB", "fuga_test_isolated")
    if test_db_name == "fuga_db":
        pytest.skip("Test DB cannot be fuga_db")
    try:
        client = AsyncIOMotorClient(mongo_uri, serverSelectionTimeoutMS=5000)
        await client.admin.command('ping')
        db = client[test_db_name]
        yield db
        await client.drop_database(test_db_name)
        client.close()
    except Exception:
        pytest.skip("Test MongoDB not available")

@pytest_asyncio.fixture
async def client(test_db):
    from app.core import database
    database.db.db = test_db
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

@pytest.mark.asyncio
async def test_register_valid(client, test_db):
    response = await client.post("/api/v1/auth/register", json={
        "email": "test@example.com",
        "password": "Password123456",
        "nombre": "Test User"
    })
    assert response.status_code == 200
    user = await test_db.usuarios.find_one({"correo": "test@example.com"})
    assert user is not None
    assert user["contrasenaHash"] != "Password123456"

@pytest.mark.asyncio
async def test_register_weak_password(client):
    response = await client.post("/api/v1/auth/register", json={
        "email": "test2@example.com",
        "password": "weak",
        "nombre": "Test User"
    })
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_register_duplicate_email(client):
    await client.post("/api/v1/auth/register", json={
        "email": "dup@example.com",
        "password": "Password123456",
        "nombre": "Test User"
    })
    response = await client.post("/api/v1/auth/register", json={
        "email": "dup@example.com",
        "password": "Password123456",
        "nombre": "Test User"
    })
    assert response.status_code == 409

@pytest.mark.asyncio
async def test_login_valid_invalid_inactive(client, test_db):
    await client.post("/api/v1/auth/register", json={
        "email": "login@example.com",
        "password": "Password123456",
        "nombre": "Test User"
    })
    response = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "Password123456"
    })
    assert response.status_code == 200
    response2 = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "WrongPass123456"
    })
    assert response2.status_code == 401
    await test_db.usuarios.update_one({"correo": "login@example.com"}, {"$set": {"estado": "inactivo"}})
    response3 = await client.post("/api/v1/auth/login", json={
        "email": "login@example.com",
        "password": "Password123456"
    })
    assert response3.status_code == 401

@pytest.mark.asyncio
async def test_protected_token_validation(client):
    response = await client.get("/api/v1/auth/me", headers={"Authorization": "Bearer invalid"})
    assert response.status_code == 401
    response2 = await client.get("/api/v1/auth/me")
    assert response2.status_code in [401, 403]

@pytest.mark.asyncio
async def test_logout_revokes_token(client):
    await client.post("/api/v1/auth/register", json={
        "email": "logout@example.com",
        "password": "Password123456",
        "nombre": "Test User"
    })
    login_res = await client.post("/api/v1/auth/login", json={
        "email": "logout@example.com",
        "password": "Password123456"
    })
    tokens = login_res.json()
    access_token = tokens["access_token"]
    me_res = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me_res.status_code == 200
    logout_res = await client.post("/api/v1/auth/logout", headers={"Authorization": f"Bearer {access_token}"})
    assert logout_res.status_code == 200
    me_res2 = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me_res2.status_code == 401

@pytest.mark.asyncio
async def test_refresh_rotation_and_old_token_rejected(client):
    await client.post("/api/v1/auth/register", json={
        "email": "refresh@example.com",
        "password": "Password123456",
        "nombre": "Test User"
    })
    login_res = await client.post("/api/v1/auth/login", json={
        "email": "refresh@example.com",
        "password": "Password123456"
    })
    tokens = login_res.json()
    old_refresh = tokens["refresh_token"]
    refresh_res = await client.post("/api/v1/auth/refresh", json={"refresh_token": old_refresh})
    assert refresh_res.status_code == 200
    new_tokens = refresh_res.json()
    assert new_tokens["refresh_token"] != old_refresh
    refresh_res2 = await client.post("/api/v1/auth/refresh", json={"refresh_token": old_refresh})
    assert refresh_res2.status_code == 401

@pytest.mark.asyncio
async def test_refresh_reuse_detection_revokes_session(client):
    await client.post("/api/v1/auth/register", json={
        "email": "reuse@example.com",
        "password": "Password123456",
        "nombre": "Test User"
    })
    login_res = await client.post("/api/v1/auth/login", json={
        "email": "reuse@example.com",
        "password": "Password123456"
    })
    tokens = login_res.json()
    old_refresh = tokens["refresh_token"]
    access_token = tokens["access_token"]
    refresh_res = await client.post("/api/v1/auth/refresh", json={"refresh_token": old_refresh})
    assert refresh_res.status_code == 200
    refresh_res_reuse = await client.post("/api/v1/auth/refresh", json={"refresh_token": old_refresh})
    assert refresh_res_reuse.status_code == 401
    me_res = await client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {access_token}"})
    assert me_res.status_code == 401

@pytest.mark.asyncio
async def test_rate_limiting(client):
    await client.post("/api/v1/auth/register", json={
        "email": "rate@example.com",
        "password": "Password123456",
        "nombre": "Test User"
    })
    for i in range(5):
        await client.post("/api/v1/auth/login", json={
            "email": "rate@example.com",
            "password": "WrongPass123456"
        })
    response = await client.post("/api/v1/auth/login", json={
        "email": "rate@example.com",
        "password": "WrongPass123456"
    })
    assert response.status_code == 429

@pytest.mark.asyncio
async def test_random_refresh_token_rejected(client):
    response = await client.post("/api/v1/auth/refresh", json={"refresh_token": "randomtoken123456789012345678901234567890"})
    assert response.status_code == 401
