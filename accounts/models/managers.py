from django.core.cache import cache
from django.db import models
from django.db.models import Sum, Avg

from ..constants import BadgeLevel


class JobSeekerProfileManager(models.Manager):
    def get_rating(self, job_seeker_id):
        from accounts.constants import CacheKeys

        cache_key = CacheKeys.JOB_SEEKER_RATING.build_key(job_seeker_id=job_seeker_id)
        rating = cache.get(cache_key)

        if rating is None:
            rating = (
                self.get_queryset()
                .get(id=job_seeker_id)
                .ratings.aggregate(Avg("rating"))["rating__avg"]
                or 0.0
            )
            cache.set(cache_key, rating, timeout=None)  # Cache forever


class SupporterProfileManager(models.Manager):
    """Custom manager for SupporterProfile model."""

    @staticmethod
    def get_total_donations(supporter_profile):
        """Calculates and caches the total donation amount for a supporter."""
        from ..constants import CacheKeys

        cache_key = CacheKeys.TOTAL_DONATIONS.build_key(
            supporter_profile_pk=supporter_profile.pk
        )
        total_donations = cache.get(cache_key)
        if total_donations is None:
            total_donations = (
                supporter_profile.donations.aggregate(total=Sum("amount"))["total"]
                or 0.00
            )
            cache.set(cache_key, total_donations, 60 * 60)  # Cache for 1 hour
        return total_donations

    @staticmethod
    def get_donation_count(supporter_profile):
        """Calculates and caches the total number of donations for a supporter."""
        from ..constants import CacheKeys

        cache_key = CacheKeys.DONATION_COUNT.build_key(
            supporter_profile_pk=supporter_profile.pk
        )
        donation_count = cache.get(cache_key)
        if donation_count is None:
            donation_count = supporter_profile.donations.count()
            cache.set(cache_key, donation_count, 60 * 60)  # Cache for 1 hour
        return donation_count

    def update_badge_level(self, supporter_profile):
        """Update badge level based on donation history and configurable thresholds."""
        total_donations = self.get_total_donations(supporter_profile)

        # Sort badge levels by their threshold in descending order
        sorted_badge_levels = sorted(
            BadgeLevel, key=lambda badge: badge.threshold, reverse=True
        )

        new_badge_level = BadgeLevel.BRONZE  # Default to bronze

        for badge in sorted_badge_levels:
            if total_donations >= badge.threshold:
                new_badge_level = badge
                break

        if supporter_profile.badge_level != new_badge_level:
            supporter_profile.badge_level = new_badge_level
            supporter_profile.save()
