import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import Uuid

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.glossary import GlossaryTerm


class GlossaryCategory(Base):
    __tablename__ = "glossary_categories"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    slug: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(100))
    sort_order: Mapped[int] = mapped_column(Integer, default=0)

    terms: Mapped[list["GlossaryTerm"]] = relationship(
        back_populates="category", order_by="GlossaryTerm.term"
    )


class GlossaryTerm(Base):
    __tablename__ = "glossary_terms"

    id: Mapped[uuid.UUID] = mapped_column(Uuid, primary_key=True, default=uuid.uuid4)
    category_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("glossary_categories.id"))
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    term: Mapped[str] = mapped_column(String(150))
    short_definition: Mapped[str] = mapped_column(String(280))
    full_explanation: Mapped[str] = mapped_column(Text)
    example: Mapped[str | None] = mapped_column(Text, nullable=True)

    category: Mapped["GlossaryCategory"] = relationship(back_populates="terms")
