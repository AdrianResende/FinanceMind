import secrets
from datetime import datetime, timezone

import jwt
from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import get_settings
from app.core.security import (
    create_access_token,
    create_password_reset_token,
    create_refresh_token,
    create_email_verification_token,
    decode_token,
)
from app.db.session import get_db
from app.integrations import google_oauth
from app.integrations.email import send_password_reset_email, send_verification_email
from app.models.user import User
from app.schemas.auth import (
    AccessTokenResponse,
    ForgotPasswordRequest,
    ResetPasswordRequest,
    UserLogin,
    UserRead,
    UserRegister,
    VerifyEmailRequest,
)
from app.services.auth_service import (
    EmailAlreadyRegisteredError,
    InvalidCredentialsError,
    authenticate_user,
    get_or_create_google_user,
    get_user_by_email,
    get_user_by_id,
    register_user,
    set_password_reset,
)

router = APIRouter(prefix="/auth", tags=["auth"])
settings = get_settings()

REFRESH_COOKIE_NAME = "refresh_token"
OAUTH_STATE_COOKIE_NAME = "oauth_state"


def _set_refresh_cookie(response: Response, token: str) -> None:
    response.set_cookie(
        key=REFRESH_COOKIE_NAME,
        value=token,
        httponly=True,
        secure=settings.environment != "development",
        samesite="lax",
        max_age=settings.refresh_token_expire_days * 24 * 60 * 60,
        path="/api/v1/auth",
    )


def _issue_tokens(response: Response, user: User) -> AccessTokenResponse:
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)
    _set_refresh_cookie(response, refresh_token)
    return AccessTokenResponse(access_token=access_token, user=UserRead.from_model(user))


@router.post("/register", response_model=AccessTokenResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister, response: Response, db: AsyncSession = Depends(get_db)):
    try:
        user = await register_user(db, payload.email, payload.password, payload.full_name)
    except EmailAlreadyRegisteredError:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Email já cadastrado")

    send_verification_email(user.email, create_email_verification_token(user.id))
    return _issue_tokens(response, user)


@router.post("/login", response_model=AccessTokenResponse)
async def login(payload: UserLogin, response: Response, db: AsyncSession = Depends(get_db)):
    try:
        user = await authenticate_user(db, payload.email, payload.password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email ou senha inválidos")

    return _issue_tokens(response, user)


@router.post("/refresh", response_model=AccessTokenResponse)
async def refresh(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    token = request.cookies.get(REFRESH_COOKIE_NAME)
    unauthorized = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Sessão expirada")
    if not token:
        raise unauthorized

    try:
        user_id = decode_token(token, expected_purpose="refresh")
    except jwt.PyJWTError:
        raise unauthorized

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise unauthorized

    return _issue_tokens(response, user)


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response):
    response.delete_cookie(REFRESH_COOKIE_NAME, path="/api/v1/auth")


@router.get("/google/login")
async def google_login(response: Response):
    state = secrets.token_urlsafe(24)
    redirect = RedirectResponse(google_oauth.build_authorization_url(state))
    redirect.set_cookie(
        key=OAUTH_STATE_COOKIE_NAME,
        value=state,
        httponly=True,
        secure=settings.environment != "development",
        samesite="lax",
        max_age=600,
        path="/api/v1/auth/google",
    )
    return redirect


@router.get("/google/callback")
async def google_callback(code: str, state: str, request: Request, db: AsyncSession = Depends(get_db)):
    expected_state = request.cookies.get(OAUTH_STATE_COOKIE_NAME)
    if not expected_state or expected_state != state:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Estado OAuth inválido")

    profile = await google_oauth.exchange_code_for_profile(code)
    user = await get_or_create_google_user(db, profile)

    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    redirect = RedirectResponse(f"{settings.frontend_url}/oauth/callback?access_token={access_token}")
    redirect.delete_cookie(OAUTH_STATE_COOKIE_NAME, path="/api/v1/auth/google")
    _set_refresh_cookie(redirect, refresh_token)
    return redirect


@router.post("/forgot-password", status_code=status.HTTP_202_ACCEPTED)
async def forgot_password(payload: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    user = await get_user_by_email(db, payload.email)
    if user is not None and user.password_hash is not None:
        send_password_reset_email(user.email, create_password_reset_token(user.id))
    return {"detail": "Se o email existir, um link de redefinição foi enviado."}


@router.post("/reset-password", status_code=status.HTTP_204_NO_CONTENT)
async def reset_password(payload: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    try:
        user_id = decode_token(payload.token, expected_purpose="password_reset")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido ou expirado")

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido ou expirado")

    await set_password_reset(db, user, payload.new_password)


@router.post("/verify-email", status_code=status.HTTP_204_NO_CONTENT)
async def verify_email(payload: VerifyEmailRequest, db: AsyncSession = Depends(get_db)):
    try:
        user_id = decode_token(payload.token, expected_purpose="email_verification")
    except jwt.PyJWTError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido ou expirado")

    user = await get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Token inválido ou expirado")

    user.email_verified_at = datetime.now(timezone.utc)
    await db.commit()
