from core.tasks import process_image_task
from core.utils.file_handling import unique_filename


class BaseProfile(models.Model):
    """Abstract base class for all user profiles with common fields"""

    # Note: user field is NOT defined here - each concrete subclass defines it
    # with their own unique related_name to avoid conflicts

    photo = models.ImageField(
        upload_to=unique_filename,
        blank=True,
        null=True,
        help_text="Profile photo of the user.",
    )
    location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Geographical location of the user.",
    )
    bio = models.TextField(
        blank=True,
        help_text="A short biography or description of the user.",
    )

    # Social media links
    linkedin_url = models.URLField(
        blank=True,
        help_text="LinkedIn profile URL.",
    )
    twitter_url = models.URLField(
        blank=True,
        help_text="Twitter profile URL.",
    )
    facebook_url = models.URLField(
        blank=True,
        help_text="Facebook profile URL.",
    )

    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the profile was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the profile was last updated.",
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.photo:
            process_image_task.delay(self.photo.path, (300, 300))

    def __str__(self):
        return f"{self.user.get_full_name()} Profile"
