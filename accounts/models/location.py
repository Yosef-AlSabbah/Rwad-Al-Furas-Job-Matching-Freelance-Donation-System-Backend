from django.db import models


class Location(models.Model):
    """
    Location Model: Geographical Data for Entities

    This model stores precise latitude and longitude coordinates and their
    corresponding human-readable address components. It serves as a central,
    reusable entity for location data across the application (e.g., for
    Coworking Spaces, user profiles, businesses).

    Key Features:
    - Stores `latitude` and `longitude` to pinpoint a location.
    - Holds derived address details like `city`, `country`, `address_line1`, etc.
    - Automatically Populates Addresses: Triggers a background geocoding task
      whenever coordinates are created or updated, ensuring address details
      are consistent and up-to-date.
    - Ensures Data Consistency: Keeps coordinates and address components synchronized.
    - Reusable: Can be linked to any other model needing location information.

    Dependencies:
    - Celery: Used for asynchronous background geocoding.
    - `geopy`: The external library used by the Celery task to perform geocoding.
    """

    latitude = models.FloatField(
        help_text="Latitude of the location.",
    )
    longitude = models.FloatField(
        help_text="Longitude of the location.",
    )
    address_line1 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="First line of the street address.",
    )
    address_line2 = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="Second line of the street address (e.g., apartment, suite).",
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="City, town, or village name.",
    )
    state_province = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="State or province name.",
    )
    postal_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        help_text="Postal code or ZIP code.",
    )
    country = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        help_text="Country name.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the location record was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the location record was last updated.",
    )



    def save(self, *args, **kwargs):
        """
        Overrides the default save method to detect changes in latitude/longitude
        and trigger background geocoding if coordinates have changed or if address
        details are missing.
        """
        is_new = self._state.adding
        old_instance = None
        if not is_new:
            old_instance = Location.objects.get(pk=self.pk)

        # Save the object first to ensure it has an ID for the task
        super().save(*args, **kwargs)

        # Trigger geocoding if:
        # 1. It's a new instance.
        # 2. Latitude or longitude has changed.
        # 3. Basic address info (city/country) is missing (in case of initial save without geocoding or failed previous geocoding)
        coordinates_changed = (
            is_new or old_instance.latitude != self.latitude or old_instance.longitude != self.longitude
        )
        address_info_missing = not self.city or not self.country

        if is_new or coordinates_changed or address_info_missing:
            # Import the task here to avoid circular imports and ensure it's loaded after models
            from ..tasks import geocode_location

            geocode_location.delay(self.id)

    def __str__(self):
        """
        Returns a human-readable string representation of the location.
        """
        parts = [self.address_line1, self.city, self.country]
        # Filter None values and join them with a comma and space
        return (
            ", ".join(filter(None, parts))
            or f"Location ({self.latitude}, {self.longitude})"
        )

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        # Add indexes for commonly queried fields to improve performance
        indexes = [
            models.Index(fields=["latitude", "longitude"]),  # For spatial queries
            models.Index(fields=["city"]),
            models.Index(fields=["country"]),
        ]
