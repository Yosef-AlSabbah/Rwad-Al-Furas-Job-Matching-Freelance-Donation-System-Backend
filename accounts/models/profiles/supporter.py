from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseProfile
from ..managers import SupporterProfileManager
from ...constants import BadgeLevel

User = get_user_model()


class SupporterProfile(BaseProfile):
    """Profile for supporters/donors"""

    # Override the user field with unique related_name
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="supporter_profile",
        help_text="The user associated with this supporter profile.",
    )

    # Supporter specific fields
    country = models.CharField(
        max_length=100,
        help_text="The country of the supporter.",
    )
    badge_level = models.CharField(
        max_length=20,
        choices=BadgeLevel.choices,
        default=BadgeLevel.BRONZE,
        help_text="The badge level achieved by the supporter based on donations.",
    )

    objects = SupporterProfileManager()  # Custom manager

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.get_badge_level_display()}"
