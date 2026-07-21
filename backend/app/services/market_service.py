import uuid
from datetime import date

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.asset import Asset
from app.models.asset_price_history import AssetPriceHistory
from app.models.benchmark_history import BenchmarkHistory


async def search_assets(db: AsyncSession, query: str | None, asset_class: str | None = None) -> list[Asset]:
    stmt = select(Asset).order_by(Asset.ticker)
    if query:
        like = f"%{query.upper()}%"
        stmt = stmt.where((Asset.ticker.ilike(like)) | (Asset.name.ilike(like)))
    if asset_class:
        stmt = stmt.where(Asset.asset_class == asset_class)
    result = await db.execute(stmt.limit(50))
    return list(result.scalars().all())


async def get_asset_by_ticker(db: AsyncSession, ticker: str) -> Asset | None:
    result = await db.execute(select(Asset).where(Asset.ticker == ticker.upper()))
    return result.scalar_one_or_none()


async def get_price_history(
    db: AsyncSession, asset_id: uuid.UUID, start: date | None = None, end: date | None = None
) -> list[AssetPriceHistory]:
    stmt = select(AssetPriceHistory).where(AssetPriceHistory.asset_id == asset_id)
    if start:
        stmt = stmt.where(AssetPriceHistory.price_date >= start)
    if end:
        stmt = stmt.where(AssetPriceHistory.price_date <= end)
    result = await db.execute(stmt.order_by(AssetPriceHistory.price_date))
    return list(result.scalars().all())


async def get_benchmark_history(
    db: AsyncSession, code: str, start: date | None = None, end: date | None = None
) -> list[BenchmarkHistory]:
    stmt = select(BenchmarkHistory).where(BenchmarkHistory.benchmark_code == code)
    if start:
        stmt = stmt.where(BenchmarkHistory.ref_date >= start)
    if end:
        stmt = stmt.where(BenchmarkHistory.ref_date <= end)
    result = await db.execute(stmt.order_by(BenchmarkHistory.ref_date))
    return list(result.scalars().all())
