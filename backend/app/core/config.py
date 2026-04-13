from pydantic_settings import BaseSettings
from functools import lru_cache
from pathlib import Path


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Newnice API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True

    # Site URLs
    SITE_URL: str = "http://localhost:3000"
    ADMIN_URL: str = "http://localhost:3000"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./autofilm.db"

    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Upload
    UPLOAD_DIR: Path = Path("uploads")
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "webp", "gif"}

    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Email (SMTP) — leave EMAIL_HOST empty to disable all email sending
    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = False       # True = SMTP_SSL (port 465)
    EMAIL_USE_STARTTLS: bool = True   # True = STARTTLS (port 587)
    EMAIL_USERNAME: str = ""
    EMAIL_PASSWORD: str = ""
    EMAIL_FROM: str = "noreply@newnice.vn"
    EMAIL_FROM_NAME: str = "Newnice"
    ADMIN_EMAIL: str = "admin@newnice.vn"  # Where new leads are sent

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
