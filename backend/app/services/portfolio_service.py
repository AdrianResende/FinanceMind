import uuid
from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.asset_price_history import AssetPriceHistory
from app.models.dividend_receipt import DividendReceipt
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction
from app.models.user import User
from app.schemas.dividend import DividendCreate
from app.schemas.market import AssetRead
from app.schemas.portfolio import PortfolioSummary, PositionItem, TransactionCreate, TransactionUpdate


class PortfolioNotFoundError(Exception):
    pass


class TransactionNotFoundError(Exception):
    pass


class InsufficientQuantityError(Exception):
    pass


class DividendNotFoundError(Exception):
    pass


async def get_default_portfolio(db: AsyncSession, user: User) -> Portfolio:
    result = await db.execute(
        select(Portfolio).where(Portfolio.user_id == user.id).order_by(Portfolio.created_at)
    )
    portfolio = result.scalars().first()
    if portfolio is None:
        raise PortfolioNotFoundError
    return portfolio


async def _get_owned_transaction(db: AsyncSession, user: User, transaction_id: uuid.UUID) -> Transaction:
    portfolio = await get_default_portfolio(db, user)
    result = await db.execute(
        select(Transaction)
        .where(Transaction.id == transaction_id, Transaction.portfolio_id == portfolio.id)
        .options(selectinload(Transaction.asset))
    )
    transaction = result.scalar_one_or_none()
    if transaction is None:
        raise TransactionNotFoundError
    return transaction


async def _current_quantity(
    db: AsyncSession,
    portfolio_id: uuid.UUID,
    asset_id: uuid.UUID,
    exclude_transaction_id: uuid.UUID | None = None,
) -> Decimal:
    stmt = select(Transaction).where(
        Transaction.portfolio_id == portfolio_id, Transaction.asset_id == asset_id
    )
    if exclude_transaction_id is not None:
        stmt = stmt.where(Transaction.id != exclude_transaction_id)
    result = await db.execute(stmt)

    quantity = Decimal("0")
    for tx in result.scalars().all():
        quantity += tx.quantity if tx.operation == "compra" else -tx.quantity
    return quantity


async def create_transaction(db: AsyncSession, user: User, payload: TransactionCreate) -> Transaction:
    portfolio = await get_default_portfolio(db, user)

    if payload.operation == "venda":
        held = await _current_quantity(db, portfolio.id, payload.asset_id)
        if payload.quantity > held:
            raise InsufficientQuantityError

    transaction = Transaction(
        portfolio_id=portfolio.id,
        asset_id=payload.asset_id,
        operation=payload.operation,
        quantity=payload.quantity,
        unit_price=payload.unit_price,
        fees=payload.fees,
        operation_date=payload.operation_date,
    )
    db.add(transaction)
    await db.commit()
    await db.refresh(transaction, attribute_names=["asset"])
    return transaction


async def update_transaction(
    db: AsyncSession, user: User, transaction_id: uuid.UUID, payload: TransactionUpdate
) -> Transaction:
    transaction = await _get_owned_transaction(db, user, transaction_id)

    new_operation = payload.operation if payload.operation is not None else transaction.operation
    new_quantity = payload.quantity if payload.quantity is not None else transaction.quantity

    if new_operation == "venda":
        held = await _current_quantity(
            db, transaction.portfolio_id, transaction.asset_id, exclude_transaction_id=transaction.id
        )
        if new_quantity > held:
            raise InsufficientQuantityError

    if payload.operation is not None:
        transaction.operation = payload.operation
    if payload.quantity is not None:
        transaction.quantity = payload.quantity
    if payload.unit_price is not None:
        transaction.unit_price = payload.unit_price
    if payload.fees is not None:
        transaction.fees = payload.fees
    if payload.operation_date is not None:
        transaction.operation_date = payload.operation_date

    await db.commit()
    await db.refresh(transaction, attribute_names=["asset"])
    return transaction


async def delete_transaction(db: AsyncSession, user: User, transaction_id: uuid.UUID) -> None:
    transaction = await _get_owned_transaction(db, user, transaction_id)
    await db.delete(transaction)
    await db.commit()


async def list_transactions(
    db: AsyncSession,
    user: User,
    asset_id: uuid.UUID | None = None,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Transaction], int]:
    portfolio = await get_default_portfolio(db, user)
    stmt = (
        select(Transaction)
        .where(Transaction.portfolio_id == portfolio.id)
        .options(selectinload(Transaction.asset))
    )
    if asset_id is not None:
        stmt = stmt.where(Transaction.asset_id == asset_id)

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()

    stmt = (
        stmt.order_by(Transaction.operation_date.desc(), Transaction.created_at.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all()), total


async def compute_position(db: AsyncSession, portfolio: Portfolio) -> PortfolioSummary:
    result = await db.execute(
        select(Transaction)
        .where(Transaction.portfolio_id == portfolio.id)
        .options(selectinload(Transaction.asset))
        .order_by(Transaction.operation_date, Transaction.created_at)
    )
    transactions = list(result.scalars().all())

    state: dict[uuid.UUID, dict] = {}
    for tx in transactions:
        entry = state.setdefault(
            tx.asset_id, {"asset": tx.asset, "quantity": Decimal("0"), "avg_price": Decimal("0")}
        )
        if tx.operation == "compra":
            total_cost = entry["quantity"] * entry["avg_price"] + tx.quantity * tx.unit_price + tx.fees
            entry["quantity"] += tx.quantity
            entry["avg_price"] = total_cost / entry["quantity"] if entry["quantity"] > 0 else Decimal("0")
        else:
            entry["quantity"] -= tx.quantity

    positions: list[PositionItem] = []
    total_invested = Decimal("0")
    total_current = Decimal("0")

    for asset_id, entry in state.items():
        quantity = entry["quantity"]
        if quantity <= 0:
            continue

        avg_price = entry["avg_price"]
        invested_value = quantity * avg_price

        price_result = await db.execute(
            select(AssetPriceHistory)
            .where(AssetPriceHistory.asset_id == asset_id)
            .order_by(AssetPriceHistory.price_date.desc())
            .limit(1)
        )
        latest_price_row = price_result.scalar_one_or_none()
        current_price = latest_price_row.close_price if latest_price_row else avg_price
        current_value = quantity * current_price
        profit = current_value - invested_value
        profit_pct = (profit / invested_value * 100) if invested_value > 0 else Decimal("0")

        positions.append(
            PositionItem(
                asset=AssetRead.from_model(entry["asset"]),
                quantity=quantity,
                avg_price=avg_price,
                invested_value=invested_value,
                current_price=current_price,
                current_value=current_value,
                profit=profit,
                profit_pct=profit_pct,
            )
        )
        total_invested += invested_value
        total_current += current_value

    total_profit = total_current - total_invested
    total_profit_pct = (total_profit / total_invested * 100) if total_invested > 0 else Decimal("0")

    return PortfolioSummary(
        positions=positions,
        total_invested=total_invested,
        total_current=total_current,
        total_profit=total_profit,
        total_profit_pct=total_profit_pct,
    )


async def create_dividend(db: AsyncSession, user: User, payload: DividendCreate) -> DividendReceipt:
    portfolio = await get_default_portfolio(db, user)

    dividend = DividendReceipt(
        portfolio_id=portfolio.id,
        asset_id=payload.asset_id,
        amount=payload.amount,
        payment_date=payload.payment_date,
    )
    db.add(dividend)
    await db.commit()
    await db.refresh(dividend, attribute_names=["asset"])
    return dividend


async def list_dividends(
    db: AsyncSession, user: User, page: int = 1, page_size: int = 20
) -> tuple[list[DividendReceipt], int]:
    portfolio = await get_default_portfolio(db, user)
    stmt = (
        select(DividendReceipt)
        .where(DividendReceipt.portfolio_id == portfolio.id)
        .options(selectinload(DividendReceipt.asset))
    )

    total = (await db.execute(select(func.count()).select_from(stmt.subquery()))).scalar_one()

    stmt = (
        stmt.order_by(DividendReceipt.payment_date.desc())
        .offset((page - 1) * page_size)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    return list(result.scalars().all()), total


async def delete_dividend(db: AsyncSession, user: User, dividend_id: uuid.UUID) -> None:
    portfolio = await get_default_portfolio(db, user)
    result = await db.execute(
        select(DividendReceipt).where(
            DividendReceipt.id == dividend_id, DividendReceipt.portfolio_id == portfolio.id
        )
    )
    dividend = result.scalar_one_or_none()
    if dividend is None:
        raise DividendNotFoundError

    await db.delete(dividend)
    await db.commit()
