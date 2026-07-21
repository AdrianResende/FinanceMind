from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.glossary import GlossaryCategoryRead, GlossaryTermDetail, GlossaryTermListItem
from app.services import glossary_service

router = APIRouter(prefix="/glossary", tags=["glossary"])


@router.get("/categories", response_model=list[GlossaryCategoryRead])
async def list_categories(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    categories = await glossary_service.list_categories(db)
    return [GlossaryCategoryRead.from_model(category) for category in categories]


@router.get("/terms", response_model=list[GlossaryTermListItem])
async def list_terms(
    category: str | None = Query(default=None),
    q: str | None = Query(default=None),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    terms = await glossary_service.list_terms(db, category, q)
    return [GlossaryTermListItem.from_model(term) for term in terms]


@router.get("/terms/{slug}", response_model=GlossaryTermDetail)
async def get_term(
    slug: str,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    term = await glossary_service.get_term_by_slug(db, slug)
    if term is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Termo não encontrado")
    return GlossaryTermDetail.from_model(term)
