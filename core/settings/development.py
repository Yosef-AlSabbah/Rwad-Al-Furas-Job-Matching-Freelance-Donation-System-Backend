"""
Development settings for Rawad Al Furas application.

This module contains development-specific settings that override
the base settings for local development with enhanced debugging.
"""

from .base import *

# Development Settings
DEBUG = True
ALLOWED_HOSTS = ["*"]

# Development Database (PostgreSQL in Docker)
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "rawad_db_dev",
        "USER": "rawad_user",
        "PASSWORD": "rawad_dev_password",
        "HOST": "rawad_database",
        "PORT": "5432",
    }
}


# Redis Settings for Development
def get_redis_url_dev(db_index: int) -> str:
    """Generate Redis URL for development environment."""
    return f"redis://:rawad_dev_redis_password@rawad_redis:6379/{db_index}"


# Override Redis configuration for development
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": get_redis_url_dev(db_index=0),
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
        "KEY_PREFIX": "rawad_dev_cache",
        "TIMEOUT": 60,  # Short timeout for development
    }
}

# Celery Settings for Development
CELERY_BROKER_URL = get_redis_url_dev(db_index=1)
CELERY_RESULT_BACKEND = get_redis_url_dev(db_index=2)
CELERY_TASK_ALWAYS_EAGER = False  # Set to True to run tasks synchronously
CELERY_TASK_EAGER_PROPAGATES = True

# CORS Settings for Development
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Static files - fix for development
STATICFILES_DIRS = []  # Remove non-existent /app/static directory
STATIC_ROOT = "/app/staticfiles"
STATIC_URL = "/static/"

# Media files
MEDIA_ROOT = "/app/media"
MEDIA_URL = "/media/"

# Development-specific apps (commented out to avoid django_extensions error)
# DEV_APPS = [
#     "django_extensions",  # Additional Django extensions for development
# ]
# INSTALLED_APPS += DEV_APPS

# Email Backend for Development
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Development Logging - Less verbose
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "simple": {
            "format": "{levelname} {asctime} {module} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",  # Changed from DEBUG to reduce verbosity
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",  # Changed from DEBUG
            "propagate": False,
        },
        "django.db.backends": {
            "handlers": ["console"],
            "level": "WARNING",  # Suppress SQL query logs
            "propagate": False,
        },
    },
}

# Django Debug Toolbar Settings
DEBUG_TOOLBAR_CONFIG = {
    "DISABLE_PANELS": [
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ],
    "SHOW_TEMPLATE_CONTEXT": True,
}

# Disable security features for development
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
