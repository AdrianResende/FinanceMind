from datetime import date
from decimal import Decimal

from sqlalchemy import select

from app.integrations.bcb_client import SGS_CODE_CDI, SGS_CODE_IPCA
from app.integrations.brapi_client import BrapiHistoryPoint, BrapiQuote
from app.integrations.tesouro_client import TesouroRow
from app.models.asset import Asset
from app.models.asset_price_history import AssetPriceHistory
from app.models.benchmark_history import BenchmarkHistory
from app.services import market_sync_service
from tests.conftest import TestSessionLocal


async def test_sync_stocks_and_funds_is_idempotent(monkeypatch):
    async def fake_get_quotes(tickers):
        return [BrapiQuote(ticker="PETR4", name="Petrobras PN", price=Decimal("38.50"), currency="BRL")]

    monkeypatch.setattr(market_sync_service.brapi_client, "get_quotes", fake_get_quotes)

    async with TestSessionLocal() as db:
        count_first = await market_sync_service.sync_stocks_and_funds(db)
        count_second = await market_sync_service.sync_stocks_and_funds(db)

        assets = (await db.execute(select(Asset))).scalars().all()
        prices = (await db.execute(select(AssetPriceHistory))).scalars().all()

    assert count_first == 1
    assert count_second == 1
    assert len(assets) == 1
    assert assets[0].ticker == "PETR4"
    assert len(prices) == 1
    assert prices[0].close_price == Decimal("38.50")


async def test_sync_tesouro_direto_upserts_asset_and_price(monkeypatch):
    async def fake_fetch_tesouro_prices():
        return [
            TesouroRow(
                titulo="Tesouro Selic",
                vencimento=date(2029, 3, 1),
                data_base=date.today(),
                pu_base=Decimal("15234.56"),
            )
        ]

    monkeypatch.setattr(market_sync_service.tesouro_client, "fetch_tesouro_prices", fake_fetch_tesouro_prices)

    async with TestSessionLocal() as db:
        count = await market_sync_service.sync_tesouro_direto(db)
        assets = (await db.execute(select(Asset))).scalars().all()

    assert count == 1
    assert len(assets) == 1
    assert assets[0].asset_class == "tesouro_direto"
    assert assets[0].ticker == "TESOURO_SELIC_2029"


async def test_sync_benchmarks_upserts_cdi_and_ipca(monkeypatch):
    today = date.today()

    async def fake_get_sgs_series(codigo, data_inicial, data_final):
        if codigo == SGS_CODE_CDI:
            return [(today, Decimal("0.05"))]
        assert codigo == SGS_CODE_IPCA
        return [(today, Decimal("0.4"))]

    monkeypatch.setattr(market_sync_service.bcb_client, "get_sgs_series", fake_get_sgs_series)

    async with TestSessionLocal() as db:
        count = await market_sync_service.sync_benchmarks(db)
        rows = (await db.execute(select(BenchmarkHistory))).scalars().all()

    assert count == 2
    codes = {row.benchmark_code for row in rows}
    assert codes == {"cdi", "ipca"}


async def test_sync_ibov_benchmark_upserts_history(monkeypatch):
    async def fake_get_history(ticker, range_="1y", interval="1d"):
        assert ticker == market_sync_service.IBOV_TICKER
        return [
            BrapiHistoryPoint(price_date=date(2026, 1, 10), close_price=Decimal("120000"), volume=None),
            BrapiHistoryPoint(price_date=date(2026, 1, 15), close_price=Decimal("126000"), volume=None),
        ]

    monkeypatch.setattr(market_sync_service.brapi_client, "get_history", fake_get_history)

    async with TestSessionLocal() as db:
        count = await market_sync_service.sync_ibov_benchmark(db)
        rows = (await db.execute(select(BenchmarkHistory))).scalars().all()

    assert count == 2
    assert {row.ref_date for row in rows} == {date(2026, 1, 10), date(2026, 1, 15)}
    assert all(row.benchmark_code == "ibov" for row in rows)
