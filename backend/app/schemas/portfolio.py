import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from app.schemas.market import AssetRead

if TYPE_CHECKING:
    from app.models.transaction import Transaction


class TransactionCreate(BaseModel):
    asset_id: uuid.UUID
    operation: str = Field(pattern="^(compra|venda)$")
    quantity: Decimal = Field(gt=0)
    unit_price: Decimal = Field(gt=0)
    fees: Decimal = Field(ge=0, default=Decimal("0"))
    operation_date: date


class TransactionUpdate(BaseModel):
    operation: str | None = Field(default=None, pattern="^(compra|venda)$")
    quantity: Decimal | None = Field(default=None, gt=0)
    unit_price: Decimal | None = Field(default=None, gt=0)
    fees: Decimal | None = Field(default=None, ge=0)
    operation_date: date | None = None


class TransactionRead(BaseModel):
    id: uuid.UUID
    asset: AssetRead
    operation: str
    quantity: Decimal
    unit_price: Decimal
    fees: Decimal
    operation_date: date

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, transaction: "Transaction") -> "TransactionRead":
        return cls(
            id=transaction.id,
            asset=AssetRead.from_model(transaction.asset),
            operation=transaction.operation,
            quantity=transaction.quantity,
            unit_price=transaction.unit_price,
            fees=transaction.fees,
            operation_date=transaction.operation_date,
        )


class TransactionListResponse(BaseModel):
    items: list[TransactionRead]
    total: int
    page: int
    page_size: int


class PositionItem(BaseModel):
    asset: AssetRead
    quantity: Decimal
    avg_price: Decimal
    invested_value: Decimal
    current_price: Decimal
    current_value: Decimal
    profit: Decimal
    profit_pct: Decimal


class PortfolioSummary(BaseModel):
    positions: list[PositionItem]
    total_invested: Decimal
    total_current: Decimal
    total_profit: Decimal
    total_profit_pct: Decimal
