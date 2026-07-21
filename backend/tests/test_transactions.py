from decimal import Decimal

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


async def _seed_asset(ticker: str = "PETR4", name: str = "Petrobras PN") -> Asset:
    async with TestSessionLocal() as db:
        asset = Asset(ticker=ticker, name=name, asset_class="acao", currency="BRL")
        db.add(asset)
        await db.commit()
        await db.refresh(asset)
        return asset


async def test_create_list_update_delete_transaction(client: AsyncClient):
    token = await _register(client, "carteira@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    asset = await _seed_asset()

    create_response = await client.post(
        "/api/v1/transactions",
        headers=headers,
        json={
            "asset_id": str(asset.id),
            "operation": "compra",
            "quantity": "10",
            "unit_price": "30.50",
            "fees": "1.50",
            "operation_date": "2026-01-10",
        },
    )
    assert create_response.status_code == 201
    transaction_id = create_response.json()["id"]
    assert create_response.json()["asset"]["ticker"] == "PETR4"

    list_response = await client.get("/api/v1/transactions", headers=headers)
    assert list_response.status_code == 200
    body = list_response.json()
    assert body["total"] == 1
    assert body["items"][0]["id"] == transaction_id

    update_response = await client.patch(
        f"/api/v1/transactions/{transaction_id}", headers=headers, json={"quantity": "5"}
    )
    assert update_response.status_code == 200
    assert Decimal(update_response.json()["quantity"]) == Decimal("5")

    delete_response = await client.delete(f"/api/v1/transactions/{transaction_id}", headers=headers)
    assert delete_response.status_code == 204

    list_after_delete = await client.get("/api/v1/transactions", headers=headers)
    assert list_after_delete.json()["total"] == 0


async def test_sell_without_holding_is_rejected(client: AsyncClient):
    token = await _register(client, "venda@example.com")
    headers = {"Authorization": f"Bearer {token}"}
    asset = await _seed_asset(ticker="VALE3", name="Vale ON")

    response = await client.post(
        "/api/v1/transactions",
        headers=headers,
        json={
            "asset_id": str(asset.id),
            "operation": "venda",
            "quantity": "5",
            "unit_price": "60",
            "operation_date": "2026-01-10",
        },
    )
    assert response.status_code == 400


async def test_transaction_ownership_is_enforced(client: AsyncClient):
    owner_token = await _register(client, "dono@example.com")
    other_token = await _register(client, "outro@example.com")
    asset = await _seed_asset(ticker="ITUB4", name="Itau PN")

    create_response = await client.post(
        "/api/v1/transactions",
        headers={"Authorization": f"Bearer {owner_token}"},
        json={
            "asset_id": str(asset.id),
            "operation": "compra",
            "quantity": "10",
            "unit_price": "30",
            "operation_date": "2026-01-10",
        },
    )
    transaction_id = create_response.json()["id"]

    response = await client.delete(
        f"/api/v1/transactions/{transaction_id}",
        headers={"Authorization": f"Bearer {other_token}"},
    )
    assert response.status_code == 404
