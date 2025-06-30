from django.db import models

from accounts.models.location import Location
from accounts.validators import validate_mobile_number, normalize_mobile_number


class WorkSpace(models.Model):
    """
    Model representing coworking spaces available for job seekers.
    Includes general information, contact details, operational hours,
    internet availability, and power availability times.
    """

    name = models.CharField(
        max_length=200,
        unique=True,
        help_text="Name of the coworking space.",
    )
    owner_name = models.CharField(
        max_length=200,
        help_text="Name of the owner or manager.",
    )
    contact_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[validate_mobile_number],
        help_text="Contact phone number for the space.",
    )

    # OneToOneField links this space to its unique location details
    location = models.OneToOneField(
        Location,
        on_delete=models.SET_NULL,  # If the Location is deleted, set this field to NULL
        null=True,  # Allows a CoworkingSpace to exist without a linked Location
        blank=True,  # Allows this field to be empty in forms
        related_name="coworking_space",  # Allows reverse lookup from Location to CoworkingSpace
        help_text="Geographic location details of the coworking space.",
    )

    has_fast_internet = models.BooleanField(
        default=True,
        help_text="Indicates if the space has fast internet.",
    )

    # Structured TimeFields for general operating hours
    opening_time = models.TimeField(
        blank=True,
        null=True,
        help_text="Daily opening time of the coworking space.",
    )
    closing_time = models.TimeField(
        blank=True,
        null=True,
        help_text="Daily closing time of the coworking space.",
    )

    # New fields for power availability hours as requested by the user
    power_start_time = models.TimeField(
        blank=True,
        null=True,
        help_text="Specific time when power becomes consistently available.",
    )
    power_end_time = models.TimeField(
        blank=True,
        null=True,
        help_text="Specific time when power is no longer consistently available.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the coworking space record was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the coworking space record was last updated.",
    )

    def __str__(self):
        """
        Returns a human-readable string representation of the coworking space.
        Includes its name and the latitude/longitude from its linked Location.
        """
        # Safely access latitude and longitude from the related Location object
        lat_long_str = "Location not set"
        if self.location:
            lat_long_str = f"({self.location.latitude}, {self.location.longitude})"
        return f"{self.name} - {lat_long_str}"

    def clean(self):
        super().clean()
        if self.contact_number:
            self.contact_number = normalize_mobile_number(self.contact_number)

    class Meta:
        verbose_name_plural = "Coworking Spaces"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["has_fast_internet"]),
            models.Index(fields=["opening_time", "closing_time"]),
            models.Index(fields=["power_start_time", "power_end_time"]),
        ]
