from datetime import date
from decimal import Decimal

from app.models.asset import Asset
from app.models.asset_price_history import AssetPriceHistory
from app.models.transaction import Transaction
from app.services import auth_service, portfolio_service
from tests.conftest import TestSessionLocal


async def test_compute_position_average_cost():
    async with TestSessionLocal() as db:
        user = await auth_service.register_user(db, "posicao@example.com", "senha12345", "Investidor")
        portfolio = await portfolio_service.get_default_portfolio(db, user)

        asset = Asset(ticker="WEGE3", name="Weg ON", asset_class="acao", currency="BRL")
        db.add(asset)
        await db.flush()

        db.add_all(
            [
                Transaction(
                    portfolio_id=portfolio.id,
                    asset_id=asset.id,
                    operation="compra",
                    quantity=Decimal("10"),
                    unit_price=Decimal("30"),
                    fees=Decimal("10"),
                    operation_date=date(2026, 1, 5),
                ),
                Transaction(
                    portfolio_id=portfolio.id,
                    asset_id=asset.id,
                    operation="compra",
                    quantity=Decimal("10"),
                    unit_price=Decimal("40"),
                    fees=Decimal("0"),
                    operation_date=date(2026, 2, 5),
                ),
                Transaction(
                    portfolio_id=portfolio.id,
                    asset_id=asset.id,
                    operation="venda",
                    quantity=Decimal("5"),
                    unit_price=Decimal("45"),
                    fees=Decimal("0"),
                    operation_date=date(2026, 3, 5),
                ),
            ]
        )
        db.add(
            AssetPriceHistory(
                asset_id=asset.id, price_date=date(2026, 3, 10), close_price=Decimal("50")
            )
        )
        await db.commit()

        summary = await portfolio_service.compute_position(db, portfolio)

    # Custo médio após as duas compras: (10*30+10 + 10*40) / 20 = 35.5
    # Venda não altera o custo médio, só reduz a quantidade: 20 - 5 = 15
    assert len(summary.positions) == 1
    position = summary.positions[0]
    assert position.quantity == Decimal("15")
    assert position.avg_price == Decimal("35.5")
    assert position.invested_value == Decimal("532.5")
    assert position.current_price == Decimal("50")
    assert position.current_value == Decimal("750.0")
    assert position.profit == Decimal("217.5")

    assert summary.total_invested == Decimal("532.5")
    assert summary.total_current == Decimal("750.0")


async def test_compute_position_falls_back_to_avg_price_without_history():
    async with TestSessionLocal() as db:
        user = await auth_service.register_user(db, "semhistorico@example.com", "senha12345", "Investidor")
        portfolio = await portfolio_service.get_default_portfolio(db, user)

        asset = Asset(ticker="MXRF11", name="Maxi Renda FII", asset_class="fii", currency="BRL")
        db.add(asset)
        await db.flush()

        db.add(
            Transaction(
                portfolio_id=portfolio.id,
                asset_id=asset.id,
                operation="compra",
                quantity=Decimal("100"),
                unit_price=Decimal("10"),
                fees=Decimal("0"),
                operation_date=date(2026, 1, 5),
            )
        )
        await db.commit()

        summary = await portfolio_service.compute_position(db, portfolio)

    position = summary.positions[0]
    assert position.current_price == position.avg_price == Decimal("10")
    assert summary.total_profit == Decimal("0")
