from datetime import date
from decimal import Decimal

import pytest
from httpx import ASGITransport, AsyncClient

from app.main import app
from app.models.asset import Asset
from app.models.asset_price_history import AssetPriceHistory
from app.models.benchmark_history import BenchmarkHistory
from app.services import auth_service, simulation_service
from app.schemas.simulation import CompoundInterestRequest
from tests.conftest import TestSessionLocal


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


async def _auth_headers(client: AsyncClient) -> dict[str, str]:
    async with TestSessionLocal() as db:
        await auth_service.register_user(db, "simulador@example.com", "senha12345", "Investidor")

    login = await client.post(
        "/api/v1/auth/login", json={"email": "simulador@example.com", "password": "senha12345"}
    )
    return {"Authorization": f"Bearer {login.json()['access_token']}"}


def test_compute_compound_interest_zero_rate_is_just_the_sum():
    payload = CompoundInterestRequest(
        initial_amount=Decimal("1000"),
        monthly_amount=Decimal("100"),
        annual_rate_pct=Decimal("0"),
        months=12,
    )
    result = simulation_service.compute_compound_interest(payload)

    assert result.final_amount == Decimal("2200")
    assert result.total_invested == Decimal("2200")
    assert result.total_interest == Decimal("0")
    assert len(result.points) == 13


def test_compute_compound_interest_with_positive_rate_generates_interest():
    payload = CompoundInterestRequest(
        initial_amount=Decimal("1000"),
        monthly_amount=Decimal("0"),
        annual_rate_pct=Decimal("12"),
        months=12,
    )
    result = simulation_service.compute_compound_interest(payload)

    assert result.total_invested == Decimal("1000")
    assert result.total_interest > Decimal("0")
    assert round(float(result.final_amount), 2) == pytest.approx(1120.0, abs=0.5)


async def test_compare_assets_computes_cumulative_return(client: AsyncClient):
    async with TestSessionLocal() as db:
        petr4 = Asset(ticker="PETR4", name="Petrobras PN", asset_class="acao", currency="BRL")
        db.add(petr4)
        await db.flush()
        db.add_all(
            [
                AssetPriceHistory(asset_id=petr4.id, price_date=date(2026, 1, 1), close_price=Decimal("30")),
                AssetPriceHistory(asset_id=petr4.id, price_date=date(2026, 1, 31), close_price=Decimal("36")),
                BenchmarkHistory(benchmark_code="cdi", ref_date=date(2026, 1, 1), value=Decimal("1")),
                BenchmarkHistory(benchmark_code="cdi", ref_date=date(2026, 1, 31), value=Decimal("1")),
            ]
        )
        await db.commit()

    headers = await _auth_headers(client)
    response = await client.post(
        "/api/v1/simulations/compare-assets",
        json={
            "tickers": ["PETR4"],
            "benchmark_codes": ["cdi"],
            "start": "2026-01-01",
            "end": "2026-01-31",
        },
        headers=headers,
    )
    assert response.status_code == 200
    body = response.json()
    series_by_key = {s["key"]: s for s in body["series"]}

    petr4_points = series_by_key["PETR4"]["points"]
    assert round(float(petr4_points[-1]["value"]), 4) == 20.0

    cdi_points = series_by_key["cdi"]["points"]
    assert round(float(cdi_points[-1]["value"]), 4) == round((1.01 * 1.01 - 1) * 100, 4)


async def test_compound_interest_endpoint_requires_auth(client: AsyncClient):
    response = await client.post(
        "/api/v1/simulations/compound-interest",
        json={
            "initial_amount": "0",
            "monthly_amount": "100",
            "annual_rate_pct": "10",
            "months": 12,
        },
    )
    assert response.status_code == 401
