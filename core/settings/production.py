"""
Production settings for Rawad Al Furas application.

This module contains production-specific settings that override
the base settings for secure and optimized production deployment.
"""

from .base import *

# Production Security Settings
DEBUG = False
ALLOWED_HOSTS = [
    "rawad.com",
    "www.rawad.com",
    "api.rawad.com",
    "localhost",
    "127.0.0.1",
]

# Security Middleware
SECURE_SSL_REDIRECT = True
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"

# Session Security
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Strict"
CSRF_COOKIE_SECURE = True
CSRF_COOKIE_HTTPONLY = True

# Database Optimization for Production
DATABASES["default"]["CONN_MAX_AGE"] = 600
DATABASES["default"]["OPTIONS"].update(
    {
        "connect_timeout": 10,
        "options": "-c default_transaction_isolation=read_committed",
    }
)

# Disable Debug Toolbar in Production
if "debug_toolbar" in INSTALLED_APPS:
    INSTALLED_APPS.remove("debug_toolbar")

if "debug_toolbar.middleware.DebugToolbarMiddleware" in MIDDLEWARE:
    MIDDLEWARE.remove("debug_toolbar.middleware.DebugToolbarMiddleware")

# CORS Settings for Production
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = [
    "https://rawad.com",
    "https://www.rawad.com",
    "https://app.rawad.com",
]

# Email Configuration for Production
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"

# Static Files Optimization
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

# Cache Optimization
CACHES["default"]["TIMEOUT"] = 900  # 15 minutes in production
CACHES["default"]["OPTIONS"]["CONNECTION_POOL_KWARGS"]["max_connections"] = 100

# Celery Production Settings
CELERY_WORKER_PREFETCH_MULTIPLIER = 1
CELERY_TASK_ACKS_LATE = True
CELERY_WORKER_DISABLE_RATE_LIMITS = False

# Production Logging
LOGGING["handlers"]["file"] = {
    "class": "logging.handlers.RotatingFileHandler",
    "filename": "/app/logs/django.log",
    "maxBytes": 1024 * 1024 * 100,  # 100MB
    "backupCount": 5,
    "formatter": "verbose",
}

LOGGING["loggers"]["django"]["handlers"] = ["console", "file"]
LOGGING["loggers"]["celery"]["handlers"] = ["console", "file"]
LOGGING["root"]["handlers"] = ["console", "file"]
