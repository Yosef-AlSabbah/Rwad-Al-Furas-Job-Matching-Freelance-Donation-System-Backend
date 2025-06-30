from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseProfile

User = get_user_model()


class IndividualClientProfile(BaseProfile):
    """Profile for individual clients and business owners"""

    class PublisherType(models.TextChoices):
        """Job publisher type choices"""

        COMPANY = "company", "Company"
        BUSINESS_OWNER = "business_owner", "Business Owner"
        INDIVIDUAL_CLIENT = "individual_client", "Individual Client"

    # Override the user field with unique related_name
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="individual_client_profile",
        help_text="The user associated with this individual client profile.",
    )

    # Individual client specific fields
    publisher_type = models.CharField(
        max_length=20,
        choices=PublisherType.choices,
        default=PublisherType.INDIVIDUAL_CLIENT,
        help_text="Type of job publisher (e.g., company, business owner, individual client).",
    )

    # Business information (for business owners)
    business_name = models.CharField(
        max_length=200,
        blank=True,
        help_text="Name of the business (if applicable).",
    )
    business_description = models.TextField(
        blank=True,
        help_text="Description of the business (if applicable).",
    )

    def __str__(self):
        if self.business_name:
            return f"{self.user.get_full_name()} - {self.business_name}"
        return f"{self.user.get_full_name()} ({self.get_publisher_type_display()})"
