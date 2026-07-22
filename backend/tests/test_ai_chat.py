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


async def _create_conversation(client: AsyncClient, headers: dict[str, str]) -> str:
    response = await client.post("/api/v1/ai/chat/conversations", headers=headers)
    assert response.status_code == 201
    return response.json()["id"]


async def test_send_message_without_groq_key_returns_fallback_and_disclaimer(client: AsyncClient):
    headers = await _register_and_login(client, "chat1@example.com")
    conversation_id = await _create_conversation(client, headers)

    response = await client.post(
        f"/api/v1/ai/chat/conversations/{conversation_id}/messages",
        json={"content": "O que é um FII?"},
        headers=headers,
    )

    assert response.status_code == 200
    body = response.json()
    assert body["role"] == "assistant"
    assert "GROQ_API_KEY" in body["content"]
    assert body["disclaimer"] is not None and "educativo" in body["disclaimer"]


async def test_conversation_history_persisted(client: AsyncClient):
    headers = await _register_and_login(client, "chat2@example.com")
    conversation_id = await _create_conversation(client, headers)

    await client.post(
        f"/api/v1/ai/chat/conversations/{conversation_id}/messages",
        json={"content": "O que é Tesouro Selic?"},
        headers=headers,
    )

    detail = await client.get(f"/api/v1/ai/chat/conversations/{conversation_id}", headers=headers)
    assert detail.status_code == 200
    messages = detail.json()["messages"]
    assert len(messages) == 2
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"
    assert detail.json()["title"] == "O que é Tesouro Selic?"


async def test_list_and_delete_conversation(client: AsyncClient):
    headers = await _register_and_login(client, "chat3@example.com")
    conversation_id = await _create_conversation(client, headers)

    listing = await client.get("/api/v1/ai/chat/conversations", headers=headers)
    assert len(listing.json()) == 1

    delete = await client.delete(f"/api/v1/ai/chat/conversations/{conversation_id}", headers=headers)
    assert delete.status_code == 204

    listing_after = await client.get("/api/v1/ai/chat/conversations", headers=headers)
    assert listing_after.json() == []


async def test_cannot_access_another_users_conversation(client: AsyncClient):
    headers_a = await _register_and_login(client, "chat4a@example.com")
    headers_b = await _register_and_login(client, "chat4b@example.com")
    conversation_id = await _create_conversation(client, headers_a)

    response = await client.get(f"/api/v1/ai/chat/conversations/{conversation_id}", headers=headers_b)
    assert response.status_code == 404


async def test_free_plan_rate_limit_returns_429_after_ten_messages(client: AsyncClient):
    headers = await _register_and_login(client, "chat5@example.com")
    conversation_id = await _create_conversation(client, headers)

    for _ in range(10):
        response = await client.post(
            f"/api/v1/ai/chat/conversations/{conversation_id}/messages",
            json={"content": "Pergunta sobre investimentos"},
            headers=headers,
        )
        assert response.status_code == 200

    eleventh = await client.post(
        f"/api/v1/ai/chat/conversations/{conversation_id}/messages",
        json={"content": "Mais uma pergunta"},
        headers=headers,
    )
    assert eleventh.status_code == 429

    usage = await client.get("/api/v1/ai/chat/usage", headers=headers)
    assert usage.json() == {"plan": "free", "used": 10, "limit": 10}
