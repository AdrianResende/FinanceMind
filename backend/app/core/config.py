from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "FinanceMind API"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"

    database_url: str = "postgresql+asyncpg://financemind:financemind@localhost:5432/financemind"
    redis_url: str = "redis://localhost:6379/0"

    jwt_secret_key: str = "change-me-in-env"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 15
    refresh_token_expire_days: int = 7

    cors_origins: list[str] = ["http://localhost:5173"]

    frontend_url: str = "http://localhost:5173"
    backend_url: str = "http://localhost:8000"

    groq_api_key: str = ""
    google_client_id: str = ""
    google_client_secret: str = ""
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    resend_api_key: str = ""
    email_from: str = "FinanceMind <onboarding@resend.dev>"

    brapi_token: str = ""
    brapi_base_url: str = "https://brapi.dev/api"

    @property
    def google_redirect_uri(self) -> str:
        return f"{self.backend_url}/api/v1/auth/google/callback"


@lru_cache
def get_settings() -> Settings:
    return Settings()
