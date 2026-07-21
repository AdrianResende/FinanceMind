import uuid
from typing import TYPE_CHECKING

from pydantic import BaseModel, EmailStr, Field

if TYPE_CHECKING:
    from app.models.user import User


class UserRegister(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    full_name: str = Field(min_length=1, max_length=255)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    full_name: str
    plan: str
    email_verified: bool

    model_config = {"from_attributes": True}

    @classmethod
    def from_model(cls, user: "User") -> "UserRead":
        return cls(
            id=user.id,
            email=user.email,
            full_name=user.full_name,
            plan=user.subscription.plan if user.subscription else "free",
            email_verified=user.email_verified_at is not None,
        )


class AccessTokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    token: str
    new_password: str = Field(min_length=8, max_length=128)


class VerifyEmailRequest(BaseModel):
    token: str
