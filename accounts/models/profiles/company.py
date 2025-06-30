from django.contrib.auth import get_user_model
from django.db import models

from core.utils.file_handling import unique_filename
from .base import BaseProfile
from accounts.models.location import Location
from core.tasks import process_image_task

User = get_user_model()


class CompanyProfile(BaseProfile):
    """Profile for companies"""

    class CompanySize(models.TextChoices):
        """Company size choices"""

        STARTUP = "startup", "1-10 employees"
        SMALL = "small", "11-50 employees"
        MEDIUM = "medium", "51-200 employees"
        LARGE = "large", "201-1000 employees"
        ENTERPRISE = "enterprise", "1000+ employees"

    # Override the user field with unique related_name
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="company_profile",
        help_text="The user associated with this company profile.",
    )

    # Company specific fields
    company_name = models.CharField(
        max_length=200,
        help_text="The official name of the company.",
    )
    company_logo = models.ImageField(
        upload_to=unique_filename,
        blank=True,
        null=True,
        help_text="Logo of the company.",
    )
    company_type = models.CharField(
        max_length=100,
        help_text="Type of company (e.g., marketing, programming).",
    )
    license_number = models.CharField(
        max_length=100,
        unique=True,
        help_text="Unique license number of the company.",
    )
    company_size = models.CharField(
        max_length=20,
        choices=CompanySize.choices,
        default=CompanySize.STARTUP,
        help_text="Size of the company based on employee count.",
    )
    headquarters = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="company_headquarters",
        help_text="Headquarters location of the company.",
    )
    website = models.URLField(
        blank=True,
        help_text="Official website URL of the company.",
    )

    class Meta:
        verbose_name = "Company Profile"
        verbose_name_plural = "Company Profiles"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Handle company logo resizing separately if needed
        if self.company_logo:
            process_image_task.delay(self.company_logo.path, (400, 400))

    def __str__(self):
        return self.company_name
