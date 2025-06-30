import phonenumbers
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_mobile_number(value):
    """
    Validate international mobile phone numbers using phonenumbers library.

    The user should provide the phone number with country code (e.g., +1234567890).
    If the number is invalid, provides helpful error messages with examples.

    Args:
        value (str): The phone number to validate

    Raises:
        ValidationError: If the phone number is invalid with helpful message
    """
    if not value:
        return  # Allow empty values, use blank=False in model if required

    try:
        # Parse the phone number (None means no default region)
        parsed_number = phonenumbers.parse(value, None)

        # Check if the number is valid
        if not phonenumbers.is_valid_number(parsed_number):
            # Get the country code to provide better error message
            try:
                country_code = parsed_number.country_code
                region_code = phonenumbers.region_code_for_country_code(country_code)

                # Get example number for the detected country
                example_number = phonenumbers.example_number(region_code)
                if example_number:
                    example_formatted = phonenumbers.format_number(
                        example_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                    )
                    raise ValidationError(
                        _(
                            "Invalid phone number. Please use international format with country code. "
                            f"Example for your country: {example_formatted}"
                        )
                    )
            except:
                pass

            raise ValidationError(
                _(
                    "Invalid phone number. Please include the country code. "
                    "Examples: +1 555 123 4567 (US), +44 20 7946 0958 (UK), "
                    "+966 50 123 4567 (Saudi Arabia)"
                )
            )

        # Check if it's a mobile number type
        number_type = phonenumbers.number_type(parsed_number)

        # Allow mobile and fixed line or mobile (some countries don't distinguish)
        allowed_types = [
            phonenumbers.PhoneNumberType.MOBILE,
            phonenumbers.PhoneNumberType.FIXED_LINE_OR_MOBILE,
        ]

        if number_type not in allowed_types:
            country_code = parsed_number.country_code
            region_code = phonenumbers.region_code_for_country_code(country_code)

            # Try to get mobile example for the country
            try:
                mobile_example = phonenumbers.example_number_for_type(
                    region_code, phonenumbers.PhoneNumberType.MOBILE
                )
                if mobile_example:
                    example_formatted = phonenumbers.format_number(
                        mobile_example, phonenumbers.PhoneNumberFormat.INTERNATIONAL
                    )
                    raise ValidationError(
                        _(
                            "Please provide a mobile phone number. "
                            f"Example mobile number for your country: {example_formatted}"
                        )
                    )
            except:
                pass

            raise ValidationError(
                _("Please provide a mobile phone number, not a landline or other type.")
            )

    except phonenumbers.NumberParseException as e:
        # Handle different parsing errors with specific messages
        if e.error_type == phonenumbers.NumberParseException.INVALID_COUNTRY_CODE:
            raise ValidationError(
                _(
                    "Invalid country code. Please start with + followed by your country code. "
                    "Examples: +1 (US/Canada), +44 (UK), +966 (Saudi Arabia), +971 (UAE)"
                )
            )
        elif e.error_type == phonenumbers.NumberParseException.NOT_A_NUMBER:
            raise ValidationError(
                _(
                    "Phone number contains invalid characters. Use only numbers, spaces, "
                    "hyphens, and parentheses. Example: +1 555 123 4567"
                )
            )
        elif e.error_type == phonenumbers.NumberParseException.TOO_SHORT_NSN:
            raise ValidationError(
                _(
                    "Phone number is too short. Please include the full number with country code. "
                    "Example: +1 555 123 4567"
                )
            )
        elif e.error_type == phonenumbers.NumberParseException.TOO_LONG:
            raise ValidationError(
                _("Phone number is too long. Please check your number and try again.")
            )
        else:
            raise ValidationError(
                _(
                    "Invalid phone number format. Please use international format with country code. "
                    "Examples: +1 555 123 4567, +44 20 7946 0958, +966 50 123 4567"
                )
            )


def normalize_mobile_number(value):
    """
    Normalize the mobile number to international E.164 format.

    Args:
        value (str): The phone number to normalize

    Returns:
        str: Normalized phone number in E.164 format (e.g., +1234567890)

    Raises:
        ValidationError: If the phone number cannot be parsed
    """
    if not value:
        return value

    try:
        parsed_number = phonenumbers.parse(value, None)

        # Return in E.164 format (international format without formatting)
        return phonenumbers.format_number(
            parsed_number, phonenumbers.PhoneNumberFormat.E164
        )
    except phonenumbers.NumberParseException:
        # If we can't parse it, validation will catch it
        return value
