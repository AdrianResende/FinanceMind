import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import CheckConstraint, Date, DateTime, ForeignKey, Numeric, String, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.asset import Asset
    from app.models.portfolio import Portfolio


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        CheckConstraint("operation IN ('compra', 'venda')", name="ck_transaction_operation"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"))
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assets.id"))
    operation: Mapped[str] = mapped_column(String(10))
    quantity: Mapped[Decimal] = mapped_column(Numeric(18, 8))
    unit_price: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    fees: Mapped[Decimal] = mapped_column(Numeric(18, 6), default=0)
    operation_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    portfolio: Mapped["Portfolio"] = relationship(back_populates="transactions")
    asset: Mapped["Asset"] = relationship(back_populates="transactions")
