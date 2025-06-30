from enum import Enum
from django.db import models


class CacheKeys(Enum):
    JOB_SEEKER_RATING = "job_seeker_{job_seeker_id}_rating"
    TOTAL_DONATIONS = "total_donations_{supporter_profile_pk}"
    DONATION_COUNT = "donation_count_{supporter_profile_pk}"

    def build_key(self, **kwargs):
        return self.value.format(**kwargs)


class BadgeLevel(models.TextChoices):
    """Badge level choices for supporters, including their donation thresholds."""

    BRONZE = "bronze", "Bronze Supporter", 0
    SILVER = "silver", "Silver Supporter", 500
    GOLD = "gold", "Gold Supporter", 2000
    PLATINUM = "platinum", "Platinum Supporter", 5000
    DIAMOND = "diamond", "Diamond Supporter", 10000

    @property
    def threshold(self):
        return self.value[2]
