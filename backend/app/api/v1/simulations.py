from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.simulation import (
    AssetComparisonRequest,
    AssetComparisonResponse,
    CompoundInterestRequest,
    CompoundInterestResponse,
)
from app.services import simulation_service

router = APIRouter(prefix="/simulations", tags=["simulations"])


@router.post("/compound-interest", response_model=CompoundInterestResponse)
async def compound_interest(
    payload: CompoundInterestRequest,
    current_user: User = Depends(get_current_user),
):
    return simulation_service.compute_compound_interest(payload)


@router.post("/compare-assets", response_model=AssetComparisonResponse)
async def compare_assets(
    payload: AssetComparisonRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await simulation_service.compute_asset_comparison(db, payload)
