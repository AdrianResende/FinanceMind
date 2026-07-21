import uuid
from typing import TYPE_CHECKING, Any

from sqlalchemy import CheckConstraint, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.asset_price_history import AssetPriceHistory
    from app.models.transaction import Transaction


class Asset(Base):
    __tablename__ = "assets"
    __table_args__ = (
        CheckConstraint(
            "asset_class IN ('acao', 'fii', 'etf', 'tesouro_direto')", name="ck_asset_class"
        ),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    ticker: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(255))
    asset_class: Mapped[str] = mapped_column(String(20))
    currency: Mapped[str] = mapped_column(String(10), default="BRL")
    asset_metadata: Mapped[dict[str, Any] | None] = mapped_column("metadata", JSON, nullable=True)

    transactions: Mapped[list["Transaction"]] = relationship(back_populates="asset")
    price_history: Mapped[list["AssetPriceHistory"]] = relationship(
        back_populates="asset", cascade="all, delete-orphan"
    )
