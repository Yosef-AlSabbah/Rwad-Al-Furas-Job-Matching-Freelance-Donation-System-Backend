from django.contrib.auth import get_user_model
from django.db import models

from .base import BaseProfile
from ..managers import JobSeekerProfileManager

User = get_user_model()


class JobSeekerProfile(BaseProfile):
    """Profile for job seekers"""

    class ExperienceLevel(models.TextChoices):
        """Experience level choices for job seekers"""

        ENTRY = "entry", "Entry Level"
        JUNIOR = "junior", "Junior"
        MID = "mid", "Mid Level"
        SENIOR = "senior", "Senior"
        EXPERT = "expert", "Expert"

    # Override the user field with unique related_name
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="job_seeker_profile",
        help_text="The user associated with this job seeker profile.",
    )
    # Job seeker specific fields
    specialization = models.CharField(
        max_length=100,
        help_text="The primary specialization of the job seeker.",
    )
    field_of_work = models.CharField(
        max_length=100,
        help_text="The field of work the job seeker is interested in.",
    )
    date_of_birth = models.DateField(
        help_text="The date of birth of the job seeker.",
    )
    experience_level = models.CharField(
        max_length=20,
        choices=ExperienceLevel.choices,
        default=ExperienceLevel.ENTRY,
        help_text="The experience level of the job seeker.",
    )
    is_available = models.BooleanField(
        default=True,
        help_text="Indicates if the job seeker is currently available for work.",
    )
    expected_hourly_rate = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
        help_text="The expected hourly rate of the job seeker.",
    )
    is_employed = models.BooleanField(
        default=False,
        help_text="Indicates if the job seeker is currently employed.",
    )
    weekly_applications_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of job applications made by the job seeker this week.",
    )
    last_application_reset = models.DateField(
        auto_now_add=True,
        help_text="The date when the weekly application count was last reset.",
    )

    objects = JobSeekerProfileManager()

    class Meta:
        verbose_name = "Job Seeker Profile"
        verbose_name_plural = "Job Seeker Profiles"

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.specialization}"


class JobSeekerService(models.Model):
    """Services offered by job seekers"""

    job_seeker = models.ForeignKey(
        JobSeekerProfile,
        on_delete=models.CASCADE,
        related_name="services",
        help_text="The job seeker offering this service.",
    )
    title = models.CharField(
        max_length=200,
        help_text="Title of the service offered.",
    )
    description = models.TextField(
        help_text="Detailed description of the service.",
    )
    portfolio_link = models.URLField(
        blank=True,
        help_text="Link to a portfolio or work sample for this service.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the service record was created.",
    )

    class Meta:
        verbose_name = "Job Seeker Service"
        verbose_name_plural = "Job Seeker Services"

    def __str__(self):
        return f"{self.job_seeker.user.get_full_name()} - {self.title}"
