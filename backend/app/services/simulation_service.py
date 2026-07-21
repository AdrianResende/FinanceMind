from datetime import date
from decimal import Decimal

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.simulation import (
    AssetComparisonRequest,
    AssetComparisonResponse,
    CompoundInterestPoint,
    CompoundInterestRequest,
    CompoundInterestResponse,
    ComparisonPoint,
    ComparisonSeries,
)
from app.services import market_service

BENCHMARK_LABELS = {"cdi": "CDI", "ipca": "IPCA", "ibov": "IBOV"}

# Benchmarks stored as period rates (compounded), unlike price series which are index levels.
COMPOUND_BENCHMARKS = {"cdi", "ipca"}


def _monthly_rate(annual_rate_pct: Decimal) -> Decimal:
    annual_rate = float(annual_rate_pct) / 100
    monthly = (1 + annual_rate) ** (1 / 12) - 1
    return Decimal(str(monthly))


def compute_compound_interest(payload: CompoundInterestRequest) -> CompoundInterestResponse:
    monthly_rate = _monthly_rate(payload.annual_rate_pct)

    balance = payload.initial_amount
    invested = payload.initial_amount
    points: list[CompoundInterestPoint] = [
        CompoundInterestPoint(month=0, invested=invested, total=balance, interest=balance - invested)
    ]

    for month in range(1, payload.months + 1):
        balance = balance * (1 + monthly_rate) + payload.monthly_amount
        invested += payload.monthly_amount
        points.append(
            CompoundInterestPoint(
                month=month,
                invested=invested,
                total=balance,
                interest=balance - invested,
            )
        )

    return CompoundInterestResponse(
        points=points,
        total_invested=invested,
        total_interest=balance - invested,
        final_amount=balance,
    )


def _cumulative_return_from_levels(rows: list[tuple[date, Decimal]]) -> list[ComparisonPoint]:
    if not rows or rows[0][1] <= 0:
        return []
    base = rows[0][1]
    return [ComparisonPoint(date=ref_date, value=(value / base - 1) * 100) for ref_date, value in rows]


def _cumulative_return_from_rates(rows: list[tuple[date, Decimal]]) -> list[ComparisonPoint]:
    cumulative = Decimal("1")
    points: list[ComparisonPoint] = []
    for ref_date, value in rows:
        cumulative *= Decimal("1") + value / Decimal("100")
        points.append(ComparisonPoint(date=ref_date, value=(cumulative - 1) * 100))
    return points


async def compute_asset_comparison(
    db: AsyncSession, payload: AssetComparisonRequest
) -> AssetComparisonResponse:
    series: list[ComparisonSeries] = []

    for ticker in payload.tickers:
        asset = await market_service.get_asset_by_ticker(db, ticker)
        if asset is None:
            continue
        history = await market_service.get_price_history(db, asset.id, payload.start, payload.end)
        rows = [(row.price_date, row.close_price) for row in history]
        series.append(
            ComparisonSeries(
                key=asset.ticker, label=asset.ticker, points=_cumulative_return_from_levels(rows)
            )
        )

    for code in payload.benchmark_codes:
        history = await market_service.get_benchmark_history(db, code, payload.start, payload.end)
        rows = [(row.ref_date, row.value) for row in history]
        points = (
            _cumulative_return_from_rates(rows)
            if code in COMPOUND_BENCHMARKS
            else _cumulative_return_from_levels(rows)
        )
        series.append(ComparisonSeries(key=code, label=BENCHMARK_LABELS[code], points=points))

    return AssetComparisonResponse(series=series)
