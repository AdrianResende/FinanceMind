import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def test_register_login_and_me_flow(client: AsyncClient):
    register_response = await client.post(
        "/api/v1/auth/register",
        json={"email": "ana@example.com", "password": "senha12345", "full_name": "Ana Investidora"},
    )
    assert register_response.status_code == 201
    body = register_response.json()
    assert body["user"]["email"] == "ana@example.com"
    assert body["user"]["plan"] == "free"
    access_token = body["access_token"]
    assert "refresh_token" in register_response.cookies

    me_response = await client.get(
        "/api/v1/users/me", headers={"Authorization": f"Bearer {access_token}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "ana@example.com"

    login_response = await client.post(
        "/api/v1/auth/login", json={"email": "ana@example.com", "password": "senha12345"}
    )
    assert login_response.status_code == 200

    wrong_password_response = await client.post(
        "/api/v1/auth/login", json={"email": "ana@example.com", "password": "errada"}
    )
    assert wrong_password_response.status_code == 401


async def test_duplicate_registration_is_rejected(client: AsyncClient):
    payload = {"email": "dup@example.com", "password": "senha12345", "full_name": "Dup"}
    first = await client.post("/api/v1/auth/register", json=payload)
    assert first.status_code == 201

    second = await client.post("/api/v1/auth/register", json=payload)
    assert second.status_code == 409


async def test_me_requires_authentication(client: AsyncClient):
    response = await client.get("/api/v1/users/me")
    assert response.status_code == 401
