import logging

from celery import shared_task
from geopy.geocoders import Nominatim

from .models.location import Location

logger = logging.getLogger(__name__)


@shared_task(
    bind=True, max_retries=3, default_retry_delay=300
)  # Retry up to 3 times, with 5 min delay
def geocode_location(self, location_id):
    """
    Celery background task to geocode a Location object using its latitude and longitude.
    It populates address_line1, city, state_province, postal_code, and country.
    """
    try:
        location_obj = Location.objects.get(id=location_id)

        # Only attempt geocoding if latitude and longitude are available
        if location_obj.latitude is not None and location_obj.longitude is not None:
            geolocator = Nominatim(
                user_agent="coworking_locator_app"
            )  # Use a unique user_agent

            try:
                # Set a timeout for the geocoding request to prevent hanging
                location_data = geolocator.reverse(
                    (location_obj.latitude, location_obj.longitude),
                    language="en",
                    exactly_one=True,  # Get the most relevant single result
                    timeout=10,  # Increased timeout to 10 seconds for reliability
                )
            except Exception as e:
                # Catch specific geocoding service errors (e.g., network issues, API limits)
                logger.error(
                    f"Geocoding service error for Location {location_id}: {e}",
                    exc_info=True,
                )
                # Retry the task if a transient error occurred
                raise self.retry(exc=e)

            if location_data and "address" in location_data.raw:
                address = location_data.raw["address"]

                # Populate the fields from the geocoding result.
                # Use .get() with a default of None to prevent KeyError if a key is missing.
                location_obj.address_line1 = address.get("road", "") + (
                    f" {address.get('house_number')}"
                    if address.get("house_number")
                    else ""
                )
                location_obj.city = (
                    address.get("city") or address.get("town") or address.get("village")
                )
                location_obj.state_province = address.get("state")
                location_obj.postal_code = address.get("postcode")
                location_obj.country = address.get("country")

                # Save only the updated fields to minimize database writes
                location_obj.save(
                    update_fields=[
                        "address_line1",
                        "city",
                        "state_province",
                        "postal_code",
                        "country",
                        "updated_at",
                    ]
                )
                logger.info(
                    f"Geocoding successful for Location {location_id}: {location_obj.city}, {location_obj.country}"
                )
            else:
                logger.warning(
                    f"No detailed address data found for Location {location_id} at {location_obj.latitude}, {location_obj.longitude}"
                )
        else:
            logger.warning(
                f"Latitude or Longitude missing for Location {location_id}. Geocoding skipped."
            )
    except Location.DoesNotExist:
        logger.error(f"Location with ID {location_id} does not exist. Task aborted.")
    except Exception:
        # Catch any other unexpected errors during task execution
        logger.exception(
            f"An unexpected error occurred during geocoding for Location {location_id}."
        )
        # For simplicity, we just log here, but in production, you'd log and potentially retry.
