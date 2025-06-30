from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from ..validators import validate_mobile_number, normalize_mobile_number

User = get_user_model()


class MobileNumber(models.Model):
    """
    Mobile number model with verification tracking

    This model handles:
    - Phone number validation with country information
    - Verification status tracking
    - One mobile number per user (replaces when updated)
    - Country and carrier information extraction
    """

    class VerificationStatus(models.TextChoices):
        """Verification status choices"""

        PENDING = "pending", "Pending Verification"
        VERIFIED = "verified", "Verified"
        EXPIRED = "expired", "Verification Expired"
        FAILED = "failed", "Verification Failed"

    # ──────────────────────────────── Database Fields ─────────────────────────────────
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="mobile_number",
        db_index=True,  # Index for better query performance
    )
    number = models.CharField(
        max_length=20,
        validators=[validate_mobile_number],
        help_text="Enter phone number with country code, e.g., +1 555 123 4567, +966 50 123 4567",
        unique=True,  # Ensure globally unique phone numbers
    )
    country_code = models.CharField(
        max_length=5,
        blank=True,
        help_text="Country code, e.g., '+966'",
    )  # e.g., "+966"
    country_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Country name, e.g., 'Saudi Arabia'",
    )  # e.g., "Saudi Arabia"
    country_iso = models.CharField(
        max_length=2,
        blank=True,
        help_text="Country ISO code, e.g., 'SA'",
    )  # e.g., "SA"
    carrier_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Carrier name, e.g., 'STC'",
    )  # e.g., "STC"
    number_type = models.CharField(
        max_length=20,
        blank=True,
        help_text="Number type, e.g., 'MOBILE'",
    )  # e.g., "MOBILE"
    is_verified = models.BooleanField(
        default=False,
        help_text="Whether the number is verified",
    )
    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        help_text="Verification status of the number",
    )
    verification_code = models.CharField(
        max_length=6,
        blank=True,
        help_text="Verification code sent to the user",
    )
    verification_code_expires = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Expiration time for the verification code",
    )
    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the number was verified",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the record was created",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the record was last updated",
    )
    last_code_generated_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Timestamp when the last verification code was generated",
    )

    class Meta:
        verbose_name = "Mobile Number"
        verbose_name_plural = "Mobile Numbers"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["number"]),
            models.Index(fields=["is_verified"]),
            models.Index(fields=["country_iso"]),
        ]
        ordering = ["-created_at"]

    def __init__(self, *args, **kwargs):
        """Store the original state when the model is instantiated."""
        super().__init__(*args, **kwargs)
        # Store the initial state of the number to check for changes
        self._original_number = self.number
        # Store the initial state of verification fields to prevent manual changes
        if not self._state.adding:
            self._store_original_verification_fields()

    def clean(self):
        """Normalize the mobile number and extract country/carrier info"""
        super().clean()
        if self.number:
            self.number = normalize_mobile_number(self.number)
            self._extract_phone_info()

    # ───────────────────────────────── Public Methods ─────────────────────────────────
    def save(self, *args, **kwargs):
        """
        Custom save method for MobileNumber.

        - Prevents creation of a MobileNumber instance with a pre-verified status.
        - Ensures verification fields can only be changed through a trusted process.
        - Automatically resets verification if the phone number changes.
        - This version avoids an extra DB query by tracking the original state in memory.
        """
        is_new = self._state.adding

        # On creation, enforce that verification fields are in their default state.
        if is_new:
            if (
                self.is_verified
                or self.verification_status != self.VerificationStatus.PENDING
                or self.verified_at is not None
            ):
                raise ValidationError(
                    _("Cannot create a mobile number with a pre-verified status.")
                )
            self.verification_code = ""
            self.verification_code_expires = None

        # On update, check for illicit changes.
        elif (
            not self._is_trusted_verification()
        ):  # Check if a trusted internal process is running
            # If the number has been changed, reset verification.
            if self._original_number != self.number:
                self._reset_verification()
            # If the number is the same, check for manual changes to verification fields.
            else:
                if (
                    self.is_verified != self._original_is_verified
                    or self.verification_status != self._original_verification_status
                    or self.verified_at != self._original_verified_at
                ):
                    raise ValidationError(
                        _(
                            "Verification status can only be changed through the verification process."
                        )
                    )

        super().save(*args, **kwargs)

        # After saving, update the "original" state in memory to match the new state.
        # This ensures consistency if the same instance is saved again.
        self._original_number = self.number
        if not is_new:
            self._store_original_verification_fields()

    def update_number(self, new_number):
        """Update the phone number and reset verification"""
        self.number = new_number
        self._reset_verification()
        self.save()
        return self

    def generate_verification_code(self):
        """Generate a 6-digit verification code"""
        import random

        # Check for cooldown
        if (
            self.last_code_generated_at
            and (timezone.now() - self.last_code_generated_at).total_seconds()
            < settings.MOBILE_NUMBER_VERIFICATION_CODE_COOLDOWN_SECONDS
        ):
            raise ValidationError(
                _(
                    f"Please wait {settings.MOBILE_NUMBER_VERIFICATION_CODE_COOLDOWN_SECONDS} seconds before generating a new code."
                )
            )

        self.verification_code = f"{random.randint(100000, 999999)}"
        self.verification_code_expires = timezone.now() + timezone.timedelta(minutes=10)
        self.verification_status = self.VerificationStatus.PENDING
        self.last_code_generated_at = timezone.now()  # Update the timestamp
        self.save()
        return self.verification_code

    def verify_code(self, code):
        """Verify the provided code"""
        if not self.verification_code:
            return False, "No verification code generated"

        if self.is_verification_expired:
            self.verification_status = self.VerificationStatus.EXPIRED
            self.save()  # Saving the "expired" status is fine
            return False, "Verification code has expired"

        if self.verification_code != code:
            return False, "Invalid verification code"

        # Set the "verifying" flag before saving.
        self._verifying = True

        try:
            # Update all the fields for successful verification
            self.is_verified = True
            self.verification_status = self.VerificationStatus.VERIFIED
            self.verified_at = timezone.now()
            self.verification_code = ""  # Clear code after successful verification
            self.verification_code_expires = None

            # Call save, which will now see the _verifying flag
            self.save()
        finally:
            # Ensure the flag is removed after the save attempt
            if hasattr(self, "_verifying"):
                del self._verifying

        return True, "Mobile number verified successfully"

    # ──────────────────────────── Private / Helper Methods ────────────────────────────
    def _is_trusted_verification(self):
        """
        Check if the current instance is being processed by a trusted internal verification process.
        Returns True if the '_verifying' attribute exists and is set to True, otherwise False.
        """
        return hasattr(self, "_verifying") and self._verifying

    def _store_original_verification_fields(self):
        """Store the original state of verification fields."""
        self._original_is_verified = self.is_verified
        self._original_verification_status = self.verification_status
        self._original_verified_at = self.verified_at

    def _reset_verification(self):
        """Reset all verification fields when phone number changes"""
        self.is_verified = False
        self.verification_status = self.VerificationStatus.PENDING
        self.verification_code = ""
        self.verification_code_expires = None
        self.verified_at = None

    def _extract_phone_info(self):
        """Extract country and carrier information from phone number"""
        import phonenumbers
        from phonenumbers import geocoder, carrier

        try:
            parsed_number = phonenumbers.parse(self.number, None)

            # Extract country information
            self.country_code = f"+{parsed_number.country_code}"
            self.country_iso = phonenumbers.region_code_for_country_code(
                parsed_number.country_code
            )
            self.country_name = geocoder.country_name_for_number(parsed_number, "en")

            # Extract carrier information
            self.carrier_name = carrier.name_for_number(parsed_number, "en")

            # Extract number type
            number_type = phonenumbers.number_type(parsed_number)
            self.number_type = number_type.name if number_type else "UNKNOWN"

        except (phonenumbers.NumberParseException, AttributeError, ImportError):
            # If extraction fails, keep the fields empty but log the specific error
            pass

    # Properties
    @property
    def is_verification_expired(self):
        """Check if verification code has expired"""
        if not self.verification_code_expires:
            return False
        return timezone.now() > self.verification_code_expires

    @property
    def formatted_number(self):
        """Return phone number in international format"""
        import phonenumbers

        try:
            parsed_number = phonenumbers.parse(self.number, None)
            return phonenumbers.format_number(
                parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
        except (phonenumbers.NumberParseException, ImportError):
            return self.number

    @property
    def national_format(self):
        """Return phone number in national format"""
        import phonenumbers

        try:
            parsed_number = phonenumbers.parse(self.number, None)
            return phonenumbers.format_number(
                parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL
            )
        except (phonenumbers.NumberParseException, ImportError):
            return self.number

    def __str__(self):
        status = "✓" if self.is_verified else "⏳"
        country = f" ({self.country_iso})" if self.country_iso else ""
        return f"{self.user.username} - {self.formatted_number}{country} {status}"


