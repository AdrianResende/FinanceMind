import uuid
from datetime import datetime

from pydantic import BaseModel, Field

DISCLAIMER = (
    "Este conteúdo é educativo e não constitui recomendação de investimento. "
    "Consulte um profissional certificado antes de tomar decisões financeiras."
)


class MessageCreate(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class MessageRead(BaseModel):
    id: uuid.UUID
    role: str
    content: str
    created_at: datetime
    disclaimer: str | None = None

    model_config = {"from_attributes": True}


class ConversationRead(BaseModel):
    id: uuid.UUID
    title: str
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationDetailRead(ConversationRead):
    messages: list[MessageRead]


class UsageRead(BaseModel):
    plan: str
    used: int
    limit: int
