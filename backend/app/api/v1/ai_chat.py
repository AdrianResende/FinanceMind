from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.v1.deps import get_current_user
from app.db.session import get_db
from app.models.user import User
from app.schemas.ai_chat import (
    ConversationDetailRead,
    ConversationRead,
    MessageCreate,
    MessageRead,
    UsageRead,
)
from app.services import ai_chat_service

router = APIRouter(prefix="/ai/chat", tags=["ai-chat"])


@router.get("/usage", response_model=UsageRead)
async def get_usage(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    used, limit = await ai_chat_service.get_usage(db, current_user)
    plan = current_user.subscription.plan if current_user.subscription else "free"
    return UsageRead(plan=plan, used=used, limit=limit)


@router.get("/conversations", response_model=list[ConversationRead])
async def list_conversations(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ai_chat_service.list_conversations(db, current_user.id)


@router.post("/conversations", response_model=ConversationRead, status_code=status.HTTP_201_CREATED)
async def create_conversation(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    return await ai_chat_service.create_conversation(db, current_user.id)


@router.get("/conversations/{conversation_id}", response_model=ConversationDetailRead)
async def get_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    from app.schemas.ai_chat import DISCLAIMER

    try:
        conversation = await ai_chat_service.get_conversation(db, current_user.id, conversation_id)
    except ai_chat_service.ConversationNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversa não encontrada")

    return ConversationDetailRead(
        id=conversation.id,
        title=conversation.title,
        created_at=conversation.created_at,
        messages=[
            MessageRead(
                id=msg.id,
                role=msg.role,
                content=msg.content,
                created_at=msg.created_at,
                disclaimer=DISCLAIMER if msg.role == "assistant" else None,
            )
            for msg in conversation.messages
        ],
    )


@router.delete("/conversations/{conversation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_conversation(
    conversation_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await ai_chat_service.delete_conversation(db, current_user.id, conversation_id)
    except ai_chat_service.ConversationNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversa não encontrada")


@router.post("/conversations/{conversation_id}/messages", response_model=MessageRead)
async def send_message(
    conversation_id: UUID,
    payload: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        message, disclaimer = await ai_chat_service.send_message(
            db, current_user, conversation_id, payload.content
        )
    except ai_chat_service.ConversationNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversa não encontrada")
    except ai_chat_service.AIRateLimitExceededError:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Limite de mensagens de IA do seu plano atingido neste mês",
        )

    return MessageRead(
        id=message.id,
        role=message.role,
        content=message.content,
        created_at=message.created_at,
        disclaimer=disclaimer,
    )
