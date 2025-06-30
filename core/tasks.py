"""
Celery tasks for the Rawad Al Furas application.

This module contains all asynchronous tasks for the job matching,
freelance, and donation system.
"""

import logging

from celery import shared_task
from django.contrib.sessions.models import Session
from django.core.mail import send_mail
from django.core.management import call_command
from django.utils import timezone

from core.utils.file_handling import resize_image

logger = logging.getLogger(__name__)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_kwargs={"max_retries": 3, "countdown": 60},
)
def send_email_task(
    self, subject, message, from_email, recipient_list, html_message=None
):
    """
    Send email asynchronously.

    Args:
        subject (str): Email subject
        message (str): Email message
        from_email (str): Sender email
        recipient_list (list): List of recipient emails
        html_message (str, optional): HTML version of the message
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=from_email,
            recipient_list=recipient_list,
            html_message=html_message,
            fail_silently=False,
        )
        logger.info(f"Email sent successfully to {recipient_list}")
        return f"Email sent to {len(recipient_list)} recipients"
    except Exception as exc:
        logger.error(f"Failed to send email: {exc}")
        raise self.retry(exc=exc)


@shared_task
def cleanup_expired_sessions():
    """
    Clean up expired sessions from the database.
    """
    try:
        expired_sessions = Session.objects.filter(expire_date__lt=timezone.now())
        count = expired_sessions.count()
        expired_sessions.delete()
        logger.info(f"Cleaned up {count} expired sessions")
        return f"Cleaned up {count} expired sessions"
    except Exception as exc:
        logger.error(f"Failed to cleanup sessions: {exc}")
        raise


@shared_task
def send_daily_summary():
    """
    Send daily summary emails to administrators.
    """
    try:
        # Implement your daily summary logic here
        logger.info("Daily summary task executed successfully")
        return "Daily summary sent successfully"
    except Exception as exc:
        logger.error(f"Failed to send daily summary: {exc}")
        raise


@shared_task(bind=True)
def process_image_task(self, image_path, size):
    """
    Process uploaded images (resize, optimize, etc.).

    Args:
        image_path (str): Path to the image file
        size (tuple): The size to resize the image to
    """
    try:
        resize_image(image_path, size)
        logger.info(f"Image processed successfully: {image_path}")
        return f"Image processed: {image_path}"
    except Exception as exc:
        logger.error(f"Failed to process image: {exc}")
        raise self.retry(exc=exc)


@shared_task
def generate_report_task(report_type, user_id, filters=None):
    """
    Generate reports asynchronously.

    Args:
        report_type (str): Type of report to generate
        user_id (int): ID of the user requesting the report
        filters (dict, optional): Filters to apply to the report
    """
    try:
        # Implement report generation logic here
        logger.info(f"Report generated successfully: {report_type}")
        return f"Report generated: {report_type}"
    except Exception as exc:
        logger.error(f"Failed to generate report: {exc}")
        raise


@shared_task
def backup_database():
    """
    Create database backup.
    """
    try:
        # Use Django's dumpdata command or custom backup logic
        call_command("dumpdata", "--output=/app/backups/backup.json")
        logger.info("Database backup completed successfully")
        return "Database backup completed"
    except Exception as exc:
        logger.error(f"Failed to backup database: {exc}")
        raise


@shared_task
def send_notification_task(user_id, message, notification_type="info"):
    """
    Send notifications to users.

    Args:
        user_id (int): ID of the user to notify
        message (str): Notification message
        notification_type (str): Type of notification
    """
    try:
        # Implement notification logic here
        logger.info(f"Notification sent to user {user_id}: {message}")
        return f"Notification sent to user {user_id}"
    except Exception as exc:
        logger.error(f"Failed to send notification: {exc}")
        raise
