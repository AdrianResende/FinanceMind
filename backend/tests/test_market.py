from datetime import date
from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.benchmark_history import BenchmarkHistory
from app.services import auth_service
from tests.conftest import TestSessionLocal


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient) -> dict[str, str]:
    async with TestSessionLocal() as db:
        await auth_service.register_user(db, "mercado@example.com", "senha12345", "Investidor")

    login = await client.post(
        "/api/v1/auth/login", json={"email": "mercado@example.com", "password": "senha12345"}
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


async def test_get_benchmark_history(client: AsyncClient):
    async with TestSessionLocal() as db:
        db.add_all(
            [
                BenchmarkHistory(benchmark_code="cdi", ref_date=date(2026, 1, 1), value=Decimal("1")),
                BenchmarkHistory(benchmark_code="cdi", ref_date=date(2026, 1, 2), value=Decimal("1")),
            ]
        )
        await db.commit()

    headers = await _auth_headers(client)
    response = await client.get("/api/v1/market/benchmarks/cdi", headers=headers)
    assert response.status_code == 200
    body = response.json()
    assert len(body) == 2
    assert body[0]["ref_date"] == "2026-01-01"


async def test_get_benchmark_history_rejects_unknown_code(client: AsyncClient):
    headers = await _auth_headers(client)
    response = await client.get("/api/v1/market/benchmarks/xyz", headers=headers)
    assert response.status_code == 404
