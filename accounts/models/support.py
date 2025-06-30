from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class SupportTicket(models.Model):
    """Technical support tickets"""

    class TicketStatus(models.TextChoices):
        """Support ticket status choices"""

        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="support_tickets",
        help_text="The user who submitted this support ticket.",
    )
    title = models.CharField(
        max_length=200,
        help_text="The subject or title of the support ticket.",
    )
    description = models.TextField(
        help_text="A brief description of the issue or request.",
    )
    message = models.TextField(
        help_text="The detailed message or content of the support ticket.",
    )
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN,
        help_text="The current status of the support ticket.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the support ticket was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the support ticket was last updated.",
    )
    

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class TicketComment(models.Model):
    """A comment on a support ticket."""

    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name="comments",
        help_text="The support ticket to which this comment belongs.",
        db_index=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="ticket_comments",
        help_text="The user who wrote the comment (ticket owner or admin).",
    )
    comment = models.TextField(
        help_text="The content of the comment.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the comment was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the comment was last updated.",
    )

    class Meta:
        ordering = ["created_at"]
        verbose_name = "Ticket Comment"
        verbose_name_plural = "Ticket Comments"

    def __str__(self):
        return f"Comment by {self.user.username} on ticket #{self.ticket.id} at {self.created_at.strftime('%Y-%m-%d %H:%M')}"

    def clean(self):
        from django.core.exceptions import ValidationError

        if self.ticket.status in [self.ticket.TicketStatus.RESOLVED, self.ticket.TicketStatus.CLOSED]:
            raise ValidationError("Cannot add comments to a resolved or closed ticket.")
