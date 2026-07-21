from datetime import date
from decimal import Decimal

from app.models.asset import Asset
from app.models.asset_price_history import AssetPriceHistory
from app.models.benchmark_history import BenchmarkHistory
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction
from app.services import auth_service, dashboard_service, portfolio_service
from tests.conftest import TestSessionLocal


async def _build_scenario():
    async with TestSessionLocal() as db:
        user = await auth_service.register_user(db, "dashboard@example.com", "senha12345", "Investidor")
        portfolio = await portfolio_service.get_default_portfolio(db, user)

        petr4 = Asset(ticker="PETR4", name="Petrobras PN", asset_class="acao", currency="BRL")
        tesouro = Asset(
            ticker="TESOURO_SELIC_2029", name="Tesouro Selic 2029", asset_class="tesouro_direto", currency="BRL"
        )
        db.add_all([petr4, tesouro])
        await db.flush()

        db.add_all(
            [
                Transaction(
                    portfolio_id=portfolio.id,
                    asset_id=petr4.id,
                    operation="compra",
                    quantity=Decimal("10"),
                    unit_price=Decimal("30"),
                    fees=Decimal("0"),
                    operation_date=date(2026, 1, 5),
                ),
                Transaction(
                    portfolio_id=portfolio.id,
                    asset_id=tesouro.id,
                    operation="compra",
                    quantity=Decimal("5"),
                    unit_price=Decimal("100"),
                    fees=Decimal("0"),
                    operation_date=date(2026, 1, 10),
                ),
            ]
        )
        db.add_all(
            [
                AssetPriceHistory(asset_id=petr4.id, price_date=date(2026, 1, 5), close_price=Decimal("30")),
                AssetPriceHistory(asset_id=petr4.id, price_date=date(2026, 1, 10), close_price=Decimal("35")),
                AssetPriceHistory(asset_id=petr4.id, price_date=date(2026, 1, 15), close_price=Decimal("40")),
                AssetPriceHistory(asset_id=tesouro.id, price_date=date(2026, 1, 10), close_price=Decimal("100")),
                AssetPriceHistory(asset_id=tesouro.id, price_date=date(2026, 1, 15), close_price=Decimal("120")),
            ]
        )
        db.add_all(
            [
                BenchmarkHistory(benchmark_code="cdi", ref_date=date(2026, 1, 10), value=Decimal("1")),
                BenchmarkHistory(benchmark_code="cdi", ref_date=date(2026, 1, 15), value=Decimal("1")),
                BenchmarkHistory(benchmark_code="ipca", ref_date=date(2026, 1, 10), value=Decimal("0.5")),
                BenchmarkHistory(benchmark_code="ipca", ref_date=date(2026, 1, 15), value=Decimal("0.5")),
                BenchmarkHistory(benchmark_code="ibov", ref_date=date(2026, 1, 10), value=Decimal("120000")),
                BenchmarkHistory(benchmark_code="ibov", ref_date=date(2026, 1, 15), value=Decimal("126000")),
            ]
        )
        await db.commit()
        return portfolio.id


async def test_get_allocation_groups_by_asset_class():
    portfolio_id = await _build_scenario()
    async with TestSessionLocal() as db:
        portfolio = await db.get(Portfolio, portfolio_id)
        allocation = await dashboard_service.get_allocation(db, portfolio)

    by_class = {item.asset_class: item for item in allocation}
    assert set(by_class) == {"acao", "tesouro_direto"}
    assert by_class["acao"].value == Decimal("400")
    assert by_class["tesouro_direto"].value == Decimal("600")
    assert round(float(by_class["acao"].percentage), 2) == 40.0
    assert round(float(by_class["tesouro_direto"].percentage), 2) == 60.0
    assert round(sum(float(item.percentage) for item in allocation), 2) == 100.0


async def test_get_performance_reconstructs_daily_value():
    portfolio_id = await _build_scenario()
    async with TestSessionLocal() as db:
        portfolio = await db.get(Portfolio, portfolio_id)
        points = await dashboard_service.get_performance(db, portfolio, date(2026, 1, 1), date(2026, 1, 31))

    values_by_date = {p.date: p.value for p in points}
    assert values_by_date[date(2026, 1, 5)] == Decimal("300")
    assert values_by_date[date(2026, 1, 10)] == Decimal("850")
    assert values_by_date[date(2026, 1, 15)] == Decimal("1000")


async def test_get_benchmarks_compounds_cdi_and_ipca_and_indexes_ibov():
    portfolio_id = await _build_scenario()
    async with TestSessionLocal() as db:
        portfolio = await db.get(Portfolio, portfolio_id)
        series = await dashboard_service.get_benchmarks(db, portfolio, date(2026, 1, 1), date(2026, 1, 31))

    portfolio_by_date = {p.date: round(float(p.value), 4) for p in series.portfolio}
    assert portfolio_by_date[date(2026, 1, 5)] == 0.0
    assert portfolio_by_date[date(2026, 1, 15)] == round((1000 / 300 - 1) * 100, 4)

    cdi_last = round(float(series.cdi[-1].value), 4)
    assert cdi_last == round((1.01 * 1.01 - 1) * 100, 4)

    ipca_last = round(float(series.ipca[-1].value), 4)
    assert ipca_last == round((1.005 * 1.005 - 1) * 100, 4)

    ibov_last = round(float(series.ibov[-1].value), 4)
    assert ibov_last == round((126000 / 120000 - 1) * 100, 4)


async def test_get_top_movers_ranks_by_latest_change():
    portfolio_id = await _build_scenario()
    async with TestSessionLocal() as db:
        portfolio = await db.get(Portfolio, portfolio_id)
        result = await dashboard_service.get_top_movers(db, portfolio)

    tickers_gainers = [item.asset.ticker for item in result.gainers]
    assert tickers_gainers[0] == "TESOURO_SELIC_2029"
    assert round(float(result.gainers[0].change_pct), 2) == 20.0

    petr4_change = next(item.change_pct for item in result.gainers if item.asset.ticker == "PETR4")
    assert round(float(petr4_change), 2) == round((40 - 35) / 35 * 100, 2)
