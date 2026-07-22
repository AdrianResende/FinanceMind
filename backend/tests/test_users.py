import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.services import auth_service
from tests.conftest import TestSessionLocal


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _register_and_login(client: AsyncClient, email: str) -> dict[str, str]:
    async with TestSessionLocal() as db:
        await auth_service.register_user(db, email, "senha12345", "Investidor")

    login = await client.post("/api/v1/auth/login", json={"email": email, "password": "senha12345"})
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


async def test_change_password_success(client: AsyncClient):
    headers = await _register_and_login(client, "senha1@example.com")

    response = await client.post(
        "/api/v1/users/me/password",
        json={"current_password": "senha12345", "new_password": "novasenha123"},
        headers=headers,
    )
    assert response.status_code == 204

    old_login = await client.post(
        "/api/v1/auth/login", json={"email": "senha1@example.com", "password": "senha12345"}
    )
    assert old_login.status_code == 401

    new_login = await client.post(
        "/api/v1/auth/login", json={"email": "senha1@example.com", "password": "novasenha123"}
    )
    assert new_login.status_code == 200


async def test_change_password_wrong_current_password(client: AsyncClient):
    headers = await _register_and_login(client, "senha2@example.com")

    response = await client.post(
        "/api/v1/users/me/password",
        json={"current_password": "senhaerrada", "new_password": "novasenha123"},
        headers=headers,
    )
    assert response.status_code == 400
