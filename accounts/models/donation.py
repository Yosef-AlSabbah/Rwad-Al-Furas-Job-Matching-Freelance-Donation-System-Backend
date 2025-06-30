from django.db import models
from django.core.validators import MinValueValidator
from .profiles import SupporterProfile


class Donation(models.Model):
    """
    Represents a donation made by a supporter.
    """

    supporter = models.ForeignKey(
        SupporterProfile,
        on_delete=models.CASCADE,
        related_name="donations",
        help_text="The supporter who made this donation.",
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0.01)],
        help_text="The amount of the donation.",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the donation was made.",
    )

    class Meta:
        verbose_name = "Donation"
        verbose_name_plural = "Donations"
        ordering = ["-timestamp"]
        indexes = [
            models.Index(fields=["supporter", "timestamp"]),
            models.Index(fields=["timestamp"]),
        ]

    def __str__(self):
        return f"Donation of {self.amount} by {self.supporter.user.get_full_name()} on {self.timestamp.strftime('%Y-%m-%d')}"
