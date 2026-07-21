import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset_price_history import AssetPriceHistory
from app.models.benchmark_history import BenchmarkHistory
from app.models.portfolio import Portfolio
from app.models.transaction import Transaction
from app.schemas.dashboard import (
    AllocationItem,
    BenchmarkPoint,
    BenchmarkSeries,
    PerformancePoint,
    TopMoverItem,
    TopMoversResponse,
)
from app.services import portfolio_service


async def get_allocation(db: AsyncSession, portfolio: Portfolio) -> list[AllocationItem]:
    summary = await portfolio_service.compute_position(db, portfolio)

    totals: dict[str, Decimal] = {}
    for position in summary.positions:
        totals[position.asset.asset_class] = (
            totals.get(position.asset.asset_class, Decimal("0")) + position.current_value
        )

    total = sum(totals.values(), Decimal("0"))
    return [
        AllocationItem(
            asset_class=asset_class,
            value=value,
            percentage=(value / total * 100) if total > 0 else Decimal("0"),
        )
        for asset_class, value in totals.items()
    ]


async def get_performance(
    db: AsyncSession, portfolio: Portfolio, start: date, end: date
) -> list[PerformancePoint]:
    tx_result = await db.execute(
        select(Transaction)
        .where(Transaction.portfolio_id == portfolio.id)
        .order_by(Transaction.operation_date)
    )
    transactions = list(tx_result.scalars().all())
    asset_ids = {tx.asset_id for tx in transactions}
    if not asset_ids:
        return []

    price_result = await db.execute(
        select(AssetPriceHistory)
        .where(AssetPriceHistory.asset_id.in_(asset_ids))
        .order_by(AssetPriceHistory.price_date)
    )
    prices_by_asset: dict[uuid.UUID, list[AssetPriceHistory]] = {}
    candidate_dates: set[date] = set()
    for row in price_result.scalars().all():
        prices_by_asset.setdefault(row.asset_id, []).append(row)
        if start <= row.price_date <= end:
            candidate_dates.add(row.price_date)

    points: list[PerformancePoint] = []
    for current_date in sorted(candidate_dates):
        total = Decimal("0")
        for asset_id in asset_ids:
            quantity = Decimal("0")
            for tx in transactions:
                if tx.asset_id != asset_id or tx.operation_date > current_date:
                    continue
                quantity += tx.quantity if tx.operation == "compra" else -tx.quantity
            if quantity <= 0:
                continue

            price = None
            for row in prices_by_asset.get(asset_id, []):
                if row.price_date > current_date:
                    break
                price = row.close_price
            if price is None:
                continue

            total += quantity * price

        points.append(PerformancePoint(date=current_date, value=total))

    return points


def _cumulative_from_levels(points: list[PerformancePoint]) -> list[BenchmarkPoint]:
    if not points or points[0].value <= 0:
        return []
    base = points[0].value
    return [BenchmarkPoint(date=p.date, value=(p.value / base - 1) * 100) for p in points]


async def _benchmark_series(
    db: AsyncSession, code: str, start: date, end: date, compound: bool
) -> list[BenchmarkPoint]:
    result = await db.execute(
        select(BenchmarkHistory)
        .where(
            BenchmarkHistory.benchmark_code == code,
            BenchmarkHistory.ref_date >= start,
            BenchmarkHistory.ref_date <= end,
        )
        .order_by(BenchmarkHistory.ref_date)
    )
    rows = list(result.scalars().all())
    if not rows:
        return []

    if compound:
        cumulative = Decimal("1")
        series = []
        for row in rows:
            cumulative *= Decimal("1") + row.value / Decimal("100")
            series.append(BenchmarkPoint(date=row.ref_date, value=(cumulative - 1) * 100))
        return series

    base = rows[0].value
    if base <= 0:
        return []
    return [BenchmarkPoint(date=row.ref_date, value=(row.value / base - 1) * 100) for row in rows]


async def get_benchmarks(db: AsyncSession, portfolio: Portfolio, start: date, end: date) -> BenchmarkSeries:
    performance = await get_performance(db, portfolio, start, end)
    return BenchmarkSeries(
        portfolio=_cumulative_from_levels(performance),
        cdi=await _benchmark_series(db, "cdi", start, end, compound=True),
        ipca=await _benchmark_series(db, "ipca", start, end, compound=True),
        ibov=await _benchmark_series(db, "ibov", start, end, compound=False),
    )


async def get_top_movers(db: AsyncSession, portfolio: Portfolio) -> TopMoversResponse:
    summary = await portfolio_service.compute_position(db, portfolio)

    movers: list[TopMoverItem] = []
    for position in summary.positions:
        result = await db.execute(
            select(AssetPriceHistory)
            .where(AssetPriceHistory.asset_id == position.asset.id)
            .order_by(AssetPriceHistory.price_date.desc())
            .limit(2)
        )
        rows = list(result.scalars().all())
        if len(rows) < 2 or rows[1].close_price == 0:
            continue

        latest, previous = rows[0], rows[1]
        change_pct = (latest.close_price - previous.close_price) / previous.close_price * 100
        movers.append(TopMoverItem(asset=position.asset, change_pct=change_pct))

    gainers = sorted(movers, key=lambda m: m.change_pct, reverse=True)[:5]
    losers = sorted(movers, key=lambda m: m.change_pct)[:5]
    return TopMoversResponse(gainers=gainers, losers=losers)
