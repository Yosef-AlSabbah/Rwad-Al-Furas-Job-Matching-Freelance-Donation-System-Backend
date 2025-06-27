"""
Core application initialization for Rawad Al Furas.

This module ensures that Celery is loaded when Django starts.
"""

# This will make sure the app is always imported when
# Django starts so that shared_task will use this app.
from .celery import app as celery_app

__all__ = ("celery_app",)
