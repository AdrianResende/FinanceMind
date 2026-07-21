import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.asset import Asset
from tests.conftest import TestSessionLocal


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _register(client: AsyncClient, email: str) -> str:
    response = await client.post(
        "/api/v1/auth/register",
        json={"email": email, "password": "senha12345", "full_name": "Investidor"},
    )
    assert response.status_code == 201
    return response.json()["access_token"]


async def _seed_asset(ticker: str = "HGLG11", name: str = "CSHG Logistica FII") -> Asset:
    async with TestSessionLocal() as db:
        asset = Asset(ticker=ticker, name=name, asset_class="fii", currency="BRL")
        db.add(asset)
        await db.commit()
        await db.refresh(asset)
        return asset


async def test_create_list_delete_dividend(client: AsyncClient):
    token = await _register(client, "dividendos@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    asset = await _seed_asset()

    create_response = await client.post(
        "/api/v1/portfolio/dividends",
        headers=headers,
        json={"asset_id": str(asset.id), "amount": "125.50", "payment_date": "2026-05-10"},
    )
    assert create_response.status_code == 201
    dividend_id = create_response.json()["id"]
    assert create_response.json()["asset"]["ticker"] == "HGLG11"

    list_response = await client.get("/api/v1/portfolio/dividends", headers=headers)
    assert list_response.status_code == 200
    body = list_response.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == dividend_id

    delete_response = await client.delete(f"/api/v1/portfolio/dividends/{dividend_id}", headers=headers)
    assert delete_response.status_code == 204

    list_after_delete = await client.get("/api/v1/portfolio/dividends", headers=headers)
    assert list_after_delete.json()["total"] == 0


async def test_dividend_ownership_is_enforced(client: AsyncClient):
    owner_token = await _register(client, "dono-div@example.com")
    other_token = await _register(client, "outro-div@example.com")
    asset = await _seed_asset(ticker="MXRF11", name="Maxi Renda FII")

    create_response = await client.post(
        "/api/v1/portfolio/dividends",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={"asset_id": str(asset.id), "amount": "10", "payment_date": "2026-05-10"},
    )
    dividend_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/v1/portfolio/dividends/{dividend_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 404
