from django.core.cache import cache
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import (
    User,
    JobSeekerProfile,
    CompanyProfile,
    IndividualClientProfile,
    SupporterProfile,
    Rating,
    Donation,
)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Automatically create the appropriate profile when a user is created
    based on their role and publisher type.
    """
    if created:
        if instance.role == "job_seeker":
            # Job seeker profile will be created manually with required fields
            pass
        elif instance.role == "job_publisher":
            # Profile creation will be handled during registration
            # since we need to determine company vs individual
            pass
        elif instance.role == "supporter":
            SupporterProfile.objects.create(
                user=instance,
                country="",  # Will be filled during registration
            )
        elif instance.role == "admin":
            # Admins don't need additional profiles
            pass


@receiver(post_save, sender=SupporterProfile)
def update_supporter_badge(sender, instance, **kwargs):
    """
    Update supporter badge level when profile is saved.
    """
    if not kwargs.get("created", False):  # Only for updates, not creation
        SupporterProfile.objects.update_badge_level(instance)


@receiver(post_save, sender=Donation)
def update_supporter_badge_on_donation(sender, instance, created, **kwargs):
    """
    Update supporter badge level when a new donation is made or an existing one is updated.
    """
    if (
        created
        or kwargs.get("update_fields") is not None
        and "amount" in kwargs.get("update_fields")
    ):
        SupporterProfile.objects.update_badge_level(instance.supporter)


@receiver(post_save, sender=Rating)
def invalidate_rating_cache(sender, instance, **kwargs):
    from accounts.constants import CacheKeys

    cache_key = CacheKeys.JOB_SEEKER_RATING.build_key(
        job_seeker_id=instance.job_seeker_id
    )
    cache.delete(cache_key)
