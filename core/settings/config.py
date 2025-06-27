"""
Configuration file for the Rawad Al Furas application using pydantic-settings.

This module defines environment variables and configuration settings
for the application using the pydantic-settings library. It provides
type-safe configuration management with validation and environment
variable parsing capabilities.
"""

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings class that inherits from BaseSettings.
    This class defines the configuration settings for the Rawad Al Furas application.
    """

    model_config = SettingsConfigDict(
        env_file=".env",  # Path to the environment file
        env_file_encoding="utf-8",  # Encoding for the environment file
        case_sensitive=True,  # Make environment variable names case-sensitive
        extra="ignore",
    )

    # Django Core Settings
    DEBUG: bool = False
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALLOWED_HOSTS: list[str] = ["*"]

    # CORS Settings
    CORS_ALLOWED_ORIGINS: list[str] = [
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://rawad.local",
    ]
    CORS_ALLOW_CREDENTIALS: bool = True

    # Django Debug Toolbar Settings
    INTERNAL_IPS: list[str] = ["127.0.0.1", "localhost"]

    # Redis Configuration
    REDIS_HOST: str = "rawad_redis"
    REDIS_PORT: int = 6379
    REDIS_PASSWORD: str = "rawad_redis_password_2025"

    # Cache Configuration
    CACHE_DB_INDEX: int = 0

    # Celery Configuration
    CELERY_BROKER_DB_INDEX: int = 1
    CELERY_RESULT_BACKEND_DB_INDEX: int = 2
    CELERY_TASK_SERIALIZER: str = "json"
    CELERY_RESULT_SERIALIZER: str = "json"
    CELERY_ACCEPT_CONTENT: list[str] = ["json"]
    CELERY_TIMEZONE: str = "UTC"
    CELERY_ENABLE_UTC: bool = True

    # PostgreSQL Database Configuration
    POSTGRES_NAME: str = "rawad_db"
    POSTGRES_USER: str = "rawad_user"
    POSTGRES_PASSWORD: str = "rawad_password_2025"
    POSTGRES_HOST: str = "rawad_database"
    POSTGRES_PORT: int = 5432

    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 100 * 1024 * 1024  # 100MB

    # Security Settings
    SECURE_BROWSER_XSS_FILTER: bool = True
    SECURE_CONTENT_TYPE_NOSNIFF: bool = True
    X_FRAME_OPTIONS: str = "DENY"

    # Email Configuration (for production)
    EMAIL_BACKEND: str = "django.core.mail.backends.console.EmailBackend"
    EMAIL_HOST: str = ""
    EMAIL_PORT: int = 587
    EMAIL_USE_TLS: bool = True
    EMAIL_HOST_USER: str = ""
    EMAIL_HOST_PASSWORD: str = ""
    DEFAULT_FROM_EMAIL: str = "noreply@rawad.com"


settings = Settings()
