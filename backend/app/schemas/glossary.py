import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel

if TYPE_CHECKING:
    from app.models.glossary import GlossaryCategory, GlossaryTerm


class GlossaryCategoryRead(BaseModel):
    id: uuid.UUID
    slug: str
    name: str

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, category: "GlossaryCategory") -> "GlossaryCategoryRead":
        return cls(id=category.id, slug=category.slug, name=category.name)


class GlossaryTermListItem(BaseModel):
    slug: str
    term: str
    short_definition: str
    category: GlossaryCategoryRead

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, term: "GlossaryTerm") -> "GlossaryTermListItem":
        return cls(
            slug=term.slug,
            term=term.term,
            short_definition=term.short_definition,
            category=GlossaryCategoryRead.from_model(term.category),
        )


class GlossaryTermDetail(GlossaryTermListItem):
    full_explanation: str
    example: str | None

    @classmethod
    def from_model(cls, term: "GlossaryTerm") -> "GlossaryTermDetail":
        return cls(
            slug=term.slug,
            term=term.term,
            short_definition=term.short_definition,
            category=GlossaryCategoryRead.from_model(term.category),
            full_explanation=term.full_explanation,
            example=term.example,
        )
