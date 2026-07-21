import uuid
from datetime import datetime, timedelta, timezone
from typing import Any, Literal

import jwt
from passlib.context import CryptContext

from app.core.config import get_settings

settings = get_settings()
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

TokenPurpose = Literal["access", "refresh", "email_verification", "password_reset"]


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, password_hash: str) -> bool:
    return pwd_context.verify(password, password_hash)


def _create_token(subject: uuid.UUID, purpose: TokenPurpose, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload: dict[str, Any] = {
        "sub": str(subject),
        "purpose": purpose,
        "iat": now,
        "exp": now + expires_delta,
    }
    return jwt.encode(payload, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)


def create_access_token(user_id: uuid.UUID) -> str:
    return _create_token(
        user_id, "access", timedelta(minutes=settings.access_token_expire_minutes)
    )


def create_refresh_token(user_id: uuid.UUID) -> str:
    return _create_token(user_id, "refresh", timedelta(days=settings.refresh_token_expire_days))


def create_email_verification_token(user_id: uuid.UUID) -> str:
    return _create_token(user_id, "email_verification", timedelta(hours=24))


def create_password_reset_token(user_id: uuid.UUID) -> str:
    return _create_token(user_id, "password_reset", timedelta(hours=1))


def decode_token(token: str, expected_purpose: TokenPurpose) -> uuid.UUID:
    payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
    if payload.get("purpose") != expected_purpose:
        raise jwt.InvalidTokenError("Unexpected token purpose")
    return uuid.UUID(payload["sub"])
