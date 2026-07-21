from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.market import AssetRead, PriceHistoryPoint
from app.services import market_service

router = APIRouter(prefix="/market", tags=["market"])


@router.get("/assets", response_model=list[AssetRead])
async def list_assets(
    q: str | None = Query(default=None),
    asset_class: str | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    assets = await market_service.search_assets(db, q, asset_class)
    return [AssetRead.from_model(asset) for asset in assets]


@router.get("/assets/{ticker}", response_model=AssetRead)
async def get_asset(
    ticker: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    asset = await market_service.get_asset_by_ticker(db, ticker)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ativo não encontrado")
    return AssetRead.from_model(asset)


@router.get("/assets/{ticker}/history", response_model=list[PriceHistoryPoint])
async def get_asset_history(
    ticker: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    asset = await market_service.get_asset_by_ticker(db, ticker)
    if asset is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ativo não encontrado")

    history = await market_service.get_price_history(db, asset.id)
    return [PriceHistoryPoint.from_model(row) for row in history]
