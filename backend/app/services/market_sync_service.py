import logging
from datetime import date, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.integrations import bcb_client, brapi_client, tesouro_client
from app.models.asset import Asset
from app.models.asset_price_history import AssetPriceHistory
from app.models.benchmark_history import BenchmarkHistory

logger = logging.getLogger("financemind.market_sync")

SEED_TICKERS: list[tuple[str, str]] = [
    ("PETR4", "acao"),
    ("VALE3", "acao"),
    ("ITUB4", "acao"),
    ("BBDC4", "acao"),
    ("ABEV3", "acao"),
    ("WEGE3", "acao"),
    ("MGLU3", "acao"),
    ("BBAS3", "acao"),
    ("B3SA3", "acao"),
    ("ITSA4", "acao"),
    ("HGLG11", "fii"),
    ("MXRF11", "fii"),
    ("KNRI11", "fii"),
    ("XPML11", "fii"),
    ("VISC11", "fii"),
    ("BOVA11", "etf"),
    ("IVVB11", "etf"),
    ("SMAL11", "etf"),
]

IBOV_TICKER = "^BVSP"


async def _upsert_asset(db: AsyncSession, ticker: str, name: str, asset_class: str, currency: str = "BRL") -> Asset:
    result = await db.execute(select(Asset).where(Asset.ticker == ticker))
    asset = result.scalar_one_or_none()
    if asset is None:
        asset = Asset(ticker=ticker, name=name, asset_class=asset_class, currency=currency)
        db.add(asset)
        await db.flush()
    else:
        asset.name = name
        asset.currency = currency
    return asset


async def _upsert_price(db: AsyncSession, asset_id, price_date: date, close_price, volume=None) -> None:
    result = await db.execute(
        select(AssetPriceHistory).where(
            AssetPriceHistory.asset_id == asset_id, AssetPriceHistory.price_date == price_date
        )
    )
    row = result.scalar_one_or_none()
    if row is None:
        db.add(AssetPriceHistory(asset_id=asset_id, price_date=price_date, close_price=close_price, volume=volume))
    else:
        row.close_price = close_price
        row.volume = volume


async def sync_stocks_and_funds(db: AsyncSession) -> int:
    tickers = [ticker for ticker, _ in SEED_TICKERS]
    asset_class_by_ticker = dict(SEED_TICKERS)
    quotes = await brapi_client.get_quotes(tickers)

    today = date.today()
    for quote in quotes:
        asset_class = asset_class_by_ticker.get(quote.ticker, "acao")
        asset = await _upsert_asset(db, quote.ticker, quote.name, asset_class, quote.currency)
        await _upsert_price(db, asset.id, today, quote.price)

    await db.commit()
    return len(quotes)


def _tesouro_ticker(titulo: str, vencimento) -> str:
    slug = titulo.upper().replace(" ", "_")
    return f"{slug}_{vencimento.year}"


async def sync_tesouro_direto(db: AsyncSession) -> int:
    rows = await tesouro_client.fetch_tesouro_prices()
    count = 0
    for row in rows:
        ticker = _tesouro_ticker(row.titulo, row.vencimento)
        name = f"{row.titulo} {row.vencimento.year}"
        asset = await _upsert_asset(db, ticker, name, "tesouro_direto")
        await _upsert_price(db, asset.id, row.data_base, row.pu_base)
        count += 1

    await db.commit()
    return count


async def _upsert_benchmark(db: AsyncSession, code: str, ref_date: date, value) -> None:
    result = await db.execute(
        select(BenchmarkHistory).where(
            BenchmarkHistory.benchmark_code == code, BenchmarkHistory.ref_date == ref_date
        )
    )
    row = result.scalar_one_or_none()
    if row is None:
        db.add(BenchmarkHistory(benchmark_code=code, ref_date=ref_date, value=value))
    else:
        row.value = value


async def sync_benchmarks(db: AsyncSession) -> int:
    end = date.today()
    start = end - timedelta(days=30)
    count = 0

    for code, sgs_code in (("cdi", bcb_client.SGS_CODE_CDI), ("ipca", bcb_client.SGS_CODE_IPCA)):
        series = await bcb_client.get_sgs_series(sgs_code, start, end)
        for ref_date, value in series:
            await _upsert_benchmark(db, code, ref_date, value)
            count += 1

    await db.commit()
    return count


async def sync_ibov_benchmark(db: AsyncSession) -> int:
    points = await brapi_client.get_history(IBOV_TICKER, range_="3mo")
    for point in points:
        await _upsert_benchmark(db, "ibov", point.price_date, point.close_price)

    await db.commit()
    return len(points)
