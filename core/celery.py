"""
Celery configuration for Rawad Al Furas application.

This module configures Celery for handling asynchronous tasks
in the job matching, freelance, and donation system.
"""

import os

from celery import Celery
from django.conf import settings

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings.production")

# Create the Celery application
app = Celery("rawad_al_furas")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
app.config_from_object("django.conf:settings", namespace="CELERY")

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Task routing configuration
app.conf.task_routes = {
    "core.tasks.send_email": {"queue": "emails"},
    "core.tasks.process_image": {"queue": "media"},
    "core.tasks.generate_report": {"queue": "reports"},
}

# Task configuration
app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone=settings.TIME_ZONE,
    enable_utc=True,
    task_track_started=True,
    task_time_limit=30 * 60,  # 30 minutes
    task_soft_time_limit=25 * 60,  # 25 minutes
    worker_prefetch_multiplier=4,
    worker_max_tasks_per_child=1000,
)


@app.task(bind=True)
def debug_task(self):
    """Debug task for testing Celery configuration."""
    print(f"Request: {self.request!r}")
    return "Celery is working correctly!"
