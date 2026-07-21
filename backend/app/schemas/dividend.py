import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import BaseModel, Field

from app.schemas.market import AssetRead

if TYPE_CHECKING:
    from app.models.dividend_receipt import DividendReceipt


class DividendCreate(BaseModel):
    asset_id: uuid.UUID
    amount: Decimal = Field(gt=0)
    payment_date: date


class DividendRead(BaseModel):
    id: uuid.UUID
    asset: AssetRead
    amount: Decimal
    payment_date: date

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, dividend: "DividendReceipt") -> "DividendRead":
        return cls(
            id=dividend.id,
            asset=AssetRead.from_model(dividend.asset),
            amount=dividend.amount,
            payment_date=dividend.payment_date,
        )


class DividendListResponse(BaseModel):
    items: list[DividendRead]
    total: int
    page: int
    page_size: int
