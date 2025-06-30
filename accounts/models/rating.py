from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from .profiles import JobSeekerProfile

User = get_user_model()


class Rating(models.Model):
    """Model to store ratings for job seekers.

    Future consideration: Only users who have worked with a specific job seeker
    (e.g., through a completed job) should be able to rate them.
    """

    rater = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="given_ratings",
        help_text="The user who gave the rating.",
    )
    job_seeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name="ratings",
        help_text="The job seeker being rated.",
    )
    rating = models.PositiveIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="The rating given, from 1 to 5.",
    )
    comment = models.TextField(
        blank=True,
        help_text="An optional comment about the rating.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the rating was created.",
    )

    class Meta:
        verbose_name = "Rating"
        verbose_name_plural = "Ratings"
        unique_together = ("rater", "job_seeker")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["rater"]),
            models.Index(fields=["job_seeker"]),
        ]

    def __str__(self):
        return f"Rating for {self.job_seeker.user.get_full_name()} by {self.rater.get_full_name()}"
