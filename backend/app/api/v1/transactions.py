from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.portfolio import TransactionCreate, TransactionListResponse, TransactionRead, TransactionUpdate
from app.services import portfolio_service

router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("", response_model=TransactionListResponse)
async def list_transactions(
    asset_id: UUID | None = Query(default=None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        transactions, total = await portfolio_service.list_transactions(
            db, current_user, asset_id=asset_id, page=page, page_size=page_size
        )
    except portfolio_service.PortfolioNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")

    return TransactionListResponse(
        items=[TransactionRead.from_model(tx) for tx in transactions],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.post("", response_model=TransactionRead, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    payload: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        transaction = await portfolio_service.create_transaction(db, current_user, payload)
    except portfolio_service.PortfolioNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Carteira não encontrada")
    except portfolio_service.InsufficientQuantityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantidade insuficiente do ativo para realizar a venda",
        )

    return TransactionRead.from_model(transaction)


@router.patch("/{transaction_id}", response_model=TransactionRead)
async def update_transaction(
    transaction_id: UUID,
    payload: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        transaction = await portfolio_service.update_transaction(db, current_user, transaction_id, payload)
    except portfolio_service.TransactionNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada")
    except portfolio_service.InsufficientQuantityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Quantidade insuficiente do ativo para realizar a venda",
        )

    return TransactionRead.from_model(transaction)


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    transaction_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await portfolio_service.delete_transaction(db, current_user, transaction_id)
    except portfolio_service.TransactionNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transação não encontrada")
