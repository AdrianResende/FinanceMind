from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.glossary import GlossaryCategory, GlossaryTerm


async def list_categories(db: AsyncSession) -> list[GlossaryCategory]:
    result = await db.execute(select(GlossaryCategory).order_by(GlossaryCategory.sort_order))
    return list(result.scalars().all())


async def list_terms(
    db: AsyncSession, category_slug: str | None = None, q: str | None = None
) -> list[GlossaryTerm]:
    stmt = select(GlossaryTerm).options(selectinload(GlossaryTerm.category))
    if category_slug:
        stmt = stmt.join(GlossaryCategory).where(GlossaryCategory.slug == category_slug)
    if q:
        like = f"%{q}%"
        stmt = stmt.where((GlossaryTerm.term.ilike(like)) | (GlossaryTerm.short_definition.ilike(like)))
    result = await db.execute(stmt.order_by(GlossaryTerm.term))
    return list(result.scalars().all())


async def get_term_by_slug(db: AsyncSession, slug: str) -> GlossaryTerm | None:
    result = await db.execute(
        select(GlossaryTerm)
        .options(selectinload(GlossaryTerm.category))
        .where(GlossaryTerm.slug == slug)
    )
    return result.scalar_one_or_none()
