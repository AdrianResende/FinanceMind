from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field, field_validator


class CompoundInterestRequest(BaseModel):
    initial_amount: Decimal = Field(ge=0)
    monthly_amount: Decimal = Field(ge=0)
    annual_rate_pct: Decimal
    months: int = Field(gt=0, le=600)


class CompoundInterestPoint(BaseModel):
    month: int
    invested: Decimal
    total: Decimal
    interest: Decimal


class CompoundInterestResponse(BaseModel):
    points: list[CompoundInterestPoint]
    total_invested: Decimal
    total_interest: Decimal
    final_amount: Decimal


class AssetComparisonRequest(BaseModel):
    tickers: list[str] = Field(default_factory=list)
    benchmark_codes: list[str] = Field(default_factory=list)
    start: date
    end: date | None = None

    @field_validator("benchmark_codes")
    @classmethod
    def validate_benchmark_codes(cls, value: list[str]) -> list[str]:
        allowed = {"cdi", "ipca", "ibov"}
        for code in value:
            if code not in allowed:
                raise ValueError(f"Indexador inválido: {code}")
        return value


class ComparisonPoint(BaseModel):
    date: date
    value: Decimal


class ComparisonSeries(BaseModel):
    key: str
    label: str
    points: list[ComparisonPoint]


class AssetComparisonResponse(BaseModel):
    series: list[ComparisonSeries]
