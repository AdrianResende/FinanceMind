import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.security import hash_password, verify_password
from app.integrations.google_oauth import GoogleProfile
from app.models.oauth_account import OAuthAccount
from app.models.portfolio import Portfolio
from app.models.subscription import Subscription
from app.models.user import User


class EmailAlreadyRegisteredError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(
        select(User).where(User.email == email).options(selectinload(User.subscription))
    )
    return result.scalar_one_or_none()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    result = await db.execute(
        select(User).where(User.id == user_id).options(selectinload(User.subscription))
    )
    return result.scalar_one_or_none()


async def register_user(db: AsyncSession, email: str, password: str, full_name: str) -> User:
    if await get_user_by_email(db, email):
        raise EmailAlreadyRegisteredError

    user = User(
        email=email,
        password_hash=hash_password(password),
        full_name=full_name,
        auth_provider="local",
    )
    user.subscription = Subscription(plan="free", status="active")
    user.portfolios.append(Portfolio(name="Carteira Principal"))
    db.add(user)
    await db.commit()
    await db.refresh(user, attribute_names=["subscription"])
    return user


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    user = await get_user_by_email(db, email)
    if user is None or user.password_hash is None or not verify_password(password, user.password_hash):
        raise InvalidCredentialsError
    return user


async def get_or_create_google_user(db: AsyncSession, profile: GoogleProfile) -> User:
    result = await db.execute(
        select(OAuthAccount).where(
            OAuthAccount.provider == "google",
            OAuthAccount.provider_user_id == profile.provider_user_id,
        )
    )
    oauth_account = result.scalar_one_or_none()
    if oauth_account is not None:
        user = await get_user_by_id(db, oauth_account.user_id)
        assert user is not None
        return user

    user = await get_user_by_email(db, profile.email)
    if user is None:
        user = User(
            email=profile.email,
            password_hash=None,
            full_name=profile.full_name,
            auth_provider="google",
        )
        user.subscription = Subscription(plan="free", status="active")
        user.portfolios.append(Portfolio(name="Carteira Principal"))
        db.add(user)

    user.oauth_accounts.append(
        OAuthAccount(provider="google", provider_user_id=profile.provider_user_id)
    )
    await db.commit()
    await db.refresh(user, attribute_names=["subscription"])
    return user


async def set_password_reset(db: AsyncSession, user: User, new_password: str) -> None:
    user.password_hash = hash_password(new_password)
    await db.commit()
