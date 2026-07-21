from datetime import date, timedelta
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.dashboard import AllocationItem, BenchmarkSeries, PerformancePoint, TopMoversResponse
from app.schemas.dividend import DividendCreate, DividendListResponse, DividendRead
from app.schemas.portfolio import PortfolioSummary
from app.services import dashboard_service, portfolio_service

router = APIRouter(prefix="/portfolio", tags=["portfolio"])

DEFAULT_PERFORMANCE_DAYS = 90


def _resolve_period(start: date | None, end: date | None) -> tuple[date, date]:
    resolved_end = end or date.today()
    resolved_start = start or resolved_end - timedelta(days=DEFAULT_PERFORMANCE_DAYS)
    return resolved_start, resolved_end


async def _get_owned_portfolio(current_user: User, db: AsyncSession):
    try:
        return await portfolio_service.get_default_portfolio(db, current_user)
    except portfolio_service.PortfolioNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")


@router.get("", response_model=PortfolioSummary)
async def get_portfolio(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    portfolio = await _get_owned_portfolio(current_user, db)
    return await portfolio_service.compute_position(db, portfolio)


@router.get("/allocation", response_model=list[AllocationItem])
async def get_allocation(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    portfolio = await _get_owned_portfolio(current_user, db)
    return await dashboard_service.get_allocation(db, portfolio)


@router.get("/performance", response_model=list[PerformancePoint])
async def get_performance(
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    portfolio = await _get_owned_portfolio(current_user, db)
    resolved_start, resolved_end = _resolve_period(start, end)
    return await dashboard_service.get_performance(db, portfolio, resolved_start, resolved_end)


@router.get("/benchmarks", response_model=BenchmarkSeries)
async def get_benchmarks(
    start: date | None = Query(default=None),
    end: date | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    portfolio = await _get_owned_portfolio(current_user, db)
    resolved_start, resolved_end = _resolve_period(start, end)
    return await dashboard_service.get_benchmarks(db, portfolio, resolved_start, resolved_end)


@router.get("/top-movers", response_model=TopMoversResponse)
async def get_top_movers(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    portfolio = await _get_owned_portfolio(current_user, db)
    return await dashboard_service.get_top_movers(db, portfolio)


@router.get("/dividends", response_model=DividendListResponse)
async def list_dividends(
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        dividends, total = await portfolio_service.list_dividends(
            db, current_user, page=page, page_size=page_size
        )
    except portfolio_service.PortfolioNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")

    return DividendListResponse(
        items=[DividendRead.from_model(d) for d in dividends],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("/dividends", response_model=DividendRead, status_code=status.HTTP_201_CREATED)
async def create_dividend(
    payload: DividendCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        dividend = await portfolio_service.create_dividend(db, current_user, payload)
    except portfolio_service.PortfolioNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")

    return DividendRead.from_model(dividend)


@router.delete("/dividends/{dividend_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_dividend(
    dividend_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await portfolio_service.delete_dividend(db, current_user, dividend_id)
    except portfolio_service.DividendNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Lançamento não encontrado")
