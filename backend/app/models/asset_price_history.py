import uuid
from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Numeric, Uuid, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.asset import Asset


class AssetPriceHistory(Base):
    __tablename__ = "asset_price_history"
    __table_args__ = (
        UniqueConstraint("asset_id", "price_date", name="uq_asset_price_history_asset_date"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    asset_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("assets.id", ondelete="CASCADE"))
    price_date: Mapped[date] = mapped_column(Date)
    close_price: Mapped[Decimal] = mapped_column(Numeric(18, 6))
    volume: Mapped[Decimal | None] = mapped_column(Numeric(20, 2), nullable=True)

    asset: Mapped["Asset"] = relationship(back_populates="price_history")
