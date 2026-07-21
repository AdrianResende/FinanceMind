import uuid
from datetime import date, datetime
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, DateTime, ForeignKey, Numeric, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.asset import Asset
    from app.models.portfolio import Portfolio


class DividendReceipt(Base):
    __tablename__ = "dividend_receipts"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    portfolio_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("portfolios.id", ondelete="CASCADE"))
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assets.id"))
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    payment_date: Mapped[date] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    portfolio: Mapped["Portfolio"] = relationship(back_populates="dividend_receipts")
    asset: Mapped["Asset"] = relationship()
