from typing import Protocol, TypedDict


class ChatMessage(TypedDict):
    role: str
    content: str


class LLMProvider(Protocol):
    async def chat(self, messages: list[ChatMessage]) -> str: ...
