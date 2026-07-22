import logging

import httpx

from app.ai.llm.base import ChatMessage
from app.core.config import get_settings

logger = logging.getLogger("financemind.ai.groq")
settings = get_settings()

UNAVAILABLE_MESSAGE = (
    "O assistente de IA ainda não está configurado neste ambiente "
    "(GROQ_API_KEY ausente). Tente novamente mais tarde."
)


class GroqProvider:
    async def chat(self, messages: list[ChatMessage]) -> str:
        if not settings.groq_api_key:
            logger.warning("GROQ_API_KEY não configurada — resposta de IA não gerada.")
            return UNAVAILABLE_MESSAGE

        url = f"{settings.groq_base_url}/chat/completions"
        headers = {"Authorization": f"Bearer {settings.groq_api_key}"}
        payload = {
            "model": settings.groq_model,
            "messages": messages,
            "temperature": 0.3,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(url, headers=headers, json=payload)
            response.raise_for_status()
            data = response.json()

        return data["choices"][0]["message"]["content"]
