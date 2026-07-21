from dataclasses import dataclass
from urllib.parse import urlencode

import httpx

from app.core.config import get_settings

settings = get_settings()

AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
TOKEN_URL = "https://oauth2.googleapis.com/token"
USERINFO_URL = "https://www.googleapis.com/oauth2/v3/userinfo"


@dataclass
class GoogleProfile:
    provider_user_id: str
    email: str
    full_name: str


def build_authorization_url(state: str) -> str:
    params = {
        "client_id": settings.google_client_id,
        "redirect_uri": settings.google_redirect_uri,
        "response_type": "code",
        "scope": "openid email profile",
        "state": state,
        "access_type": "online",
        "prompt": "select_account",
    }
    return f"{AUTH_URL}?{urlencode(params)}"


async def exchange_code_for_profile(code: str) -> GoogleProfile:
    async with httpx.AsyncClient(timeout=10) as client:
        token_response = await client.post(
            TOKEN_URL,
            data={
                "code": code,
                "client_id": settings.google_client_id,
                "client_secret": settings.google_client_secret,
                "redirect_uri": settings.google_redirect_uri,
                "grant_type": "authorization_code",
            },
        )
        token_response.raise_for_status()
        access_token = token_response.json()["access_token"]

        userinfo_response = await client.get(
            USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"}
        )
        userinfo_response.raise_for_status()
        data = userinfo_response.json()

    return GoogleProfile(
        provider_user_id=data["sub"],
        email=data["email"],
        full_name=data.get("name", data["email"]),
    )
