import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.models.asset import Asset
    from app.models.asset_price_history import AssetPriceHistory
    from app.models.benchmark_history import BenchmarkHistory


class AssetRead(BaseModel):
    id: uuid.UUID
    ticker: str
    name: str
    asset_class: str
    currency: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, asset: "Asset") -> "AssetRead":
        return cls(
            id=asset.id,
            ticker=asset.ticker,
            name=asset.name,
            asset_class=asset.asset_class,
            currency=asset.currency,
        )


class PriceHistoryPoint(BaseModel):
    price_date: date
    close_price: Decimal

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, row: "AssetPriceHistory") -> "PriceHistoryPoint":
        return cls(price_date=row.price_date, close_price=row.close_price)


class BenchmarkPoint(BaseModel):
    ref_date: date
    value: Decimal

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, row: "BenchmarkHistory") -> "BenchmarkPoint":
        return cls(ref_date=row.ref_date, value=row.value)
