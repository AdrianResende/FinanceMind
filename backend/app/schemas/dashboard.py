from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.schemas.market import AssetRead


class AllocationItem(BaseModel):
    asset_class: str
    value: Decimal
    percentage: Decimal


class PerformancePoint(BaseModel):
    date: date
    value: Decimal


class BenchmarkPoint(BaseModel):
    date: date
    value: Decimal


class BenchmarkSeries(BaseModel):
    portfolio: list[BenchmarkPoint]
    cdi: list[BenchmarkPoint]
    ipca: list[BenchmarkPoint]
    ibov: list[BenchmarkPoint]


class TopMoverItem(BaseModel):
    asset: AssetRead
    change_pct: Decimal


class TopMoversResponse(BaseModel):
    gainers: list[TopMoverItem]
    losers: list[TopMoverItem]
