from pydantic_settings import BaseSettings
from pydantic import model_validator, field_validator
from functools import lru_cache
from pathlib import Path
import re


class Settings(BaseSettings):
    # App
    APP_NAME: str = "Newnice API"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = False

    # Site URLs
    SITE_URL: str = "http://localhost:3000"
    ADMIN_URL: str = "http://localhost:3000"

    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./autofilm.db"

    # Security
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours

    # Upload
    UPLOAD_DIR: Path = Path("uploads")
    UPLOAD_STORAGE: str = "local"  # local | r2
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"jpg", "jpeg", "png", "webp", "gif"}

    # Cloudflare R2 (S3-compatible)
    R2_ACCOUNT_ID: str = ""
    R2_ACCESS_KEY_ID: str = ""
    R2_SECRET_ACCESS_KEY: str = ""
    R2_BUCKET_NAME: str = ""
    R2_PUBLIC_URL: str = ""
    R2_ENDPOINT_URL: str = ""

    # CORS - comma-separated list or JSON array in environment
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

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        """Parse CORS_ORIGINS from comma-separated string or list."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @model_validator(mode="after")
    def validate_security_settings(self):
        """Validate security settings for production."""
        insecure_keys = {
            "",
            "change-this-secret-key-in-production",
            "your-secret-key-change-in-production",
            "dev-secret-key-change-in-production",
        }

        if not self.DEBUG and self.SECRET_KEY in insecure_keys:
            raise ValueError("SECRET_KEY must be set to a strong value when DEBUG is False")

        # Ensure SECRET_KEY is strong enough (at least 32 characters)
        if not self.DEBUG and len(self.SECRET_KEY) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long in production")

        # Validate URLs are HTTPS in production
        if not self.DEBUG:
            for url_name, url_value in [("SITE_URL", self.SITE_URL), ("ADMIN_URL", self.ADMIN_URL)]:
                if not url_value.startswith("https://"):
                    raise ValueError(f"{url_name} must use HTTPS in production")

        # Validate CORS_ORIGINS - no wildcard in production
        if not self.DEBUG and "*" in self.CORS_ORIGINS:
            raise ValueError("CORS wildcard (*) is not allowed in production")

        if self.UPLOAD_STORAGE not in {"local", "r2"}:
            raise ValueError("UPLOAD_STORAGE must be either 'local' or 'r2'")

        if self.UPLOAD_STORAGE == "r2":
            required_r2_fields = {
                "R2_ACCOUNT_ID": self.R2_ACCOUNT_ID,
                "R2_ACCESS_KEY_ID": self.R2_ACCESS_KEY_ID,
                "R2_SECRET_ACCESS_KEY": self.R2_SECRET_ACCESS_KEY,
                "R2_BUCKET_NAME": self.R2_BUCKET_NAME,
                "R2_PUBLIC_URL": self.R2_PUBLIC_URL,
            }
            missing = [name for name, value in required_r2_fields.items() if not value]
            if missing:
                raise ValueError(f"Missing required R2 settings: {', '.join(missing)}")

        return self

    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()

