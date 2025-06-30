import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Extended User model with a UUID primary key and role-based system.

    The `id` field is a UUID, providing a unique, non-sequential identifier for each user.

    Inherited from AbstractUser:
    - username: Unique username for login
    - first_name: User's first name
    - last_name: User's last name
    - email: User's email address
    - is_staff: Boolean indicating if user can access admin site
    - is_active: Boolean indicating if user account is active
    - is_superuser: Boolean indicating if user has all permissions
    - last_login: DateTime of user's last login
    - date_joined: DateTime when user account was created
    - password: Hashed password
    - groups: Many-to-many relationship to Group model
    - user_permissions: Many-to-many relationship to Permission model

    Custom fields:
    - id: UUID primary key
    - role: User's role in the platform (job_seeker, job_publisher, supporter, admin)
    - mobile_number: One-to-one relationship to MobileNumber model (user's mobile number)
    - is_verified: Boolean indicating if user's account is verified
    - created_at: DateTime when this record was created
    - updated_at: DateTime when this record was last updated
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class UserRole(models.TextChoices):
        """User role choices for the platform"""

        JOB_SEEKER = "job_seeker", "Job Seeker"
        JOB_PUBLISHER = "job_publisher", "Job Publisher"
        SUPPORTER = "supporter", "Supporter"
        STAFF = (
            "staff",
            "Staff",
        )  # Here to generalize the thing we can say staff or emplyee or some generic thing

    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.JOB_SEEKER,
        help_text="The role of the user in the platform.",
    )
    is_verified = models.BooleanField(
        default=False,
        help_text="Designates whether this user has verified their account.",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="The date and time when the user account was created.",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="The date and time when the user account was last updated.",
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
