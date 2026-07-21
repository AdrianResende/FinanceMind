import uuid
from datetime import date
from decimal import Decimal

from sqlalchemy import CheckConstraint, Date, Numeric, String, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class BenchmarkHistory(Base):
    __tablename__ = "benchmark_history"
    __table_args__ = (
        UniqueConstraint("benchmark_code", "ref_date", name="uq_benchmark_history_code_date"),
        CheckConstraint("benchmark_code IN ('cdi', 'ipca', 'ibov')", name="ck_benchmark_code"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    benchmark_code: Mapped[str] = mapped_column(String(10))
    ref_date: Mapped[date] = mapped_column(Date)
    value: Mapped[Decimal] = mapped_column(Numeric(18, 8))
