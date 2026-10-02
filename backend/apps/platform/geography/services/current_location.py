"""
One-time current-location service.

The service accepts coordinates obtained by the browser/device Geolocation API.
It does not poll, stream, track, or persist location history.
"""

from __future__ import annotations

from decimal import Decimal

from apps.platform.geography.exceptions import InvalidCoordinatesError
from apps.platform.geography.services.geocoding import ReverseGeocodingService
from apps.platform.geography.services.normalization import normalize_reverse_geocode
from apps.platform.geography.services.reference_resolution import (
    resolve_reference_entities,
)


class CurrentLocationService:
    """Resolve a single current device location."""

    def __init__(self, geocoding_service=None) -> None:
        self.geocoding_service = geocoding_service or ReverseGeocodingService()

    def resolve(
        self,
        *,
        latitude,
        longitude,
        accuracy_meters: float | None = None,
    ) -> dict:
        """Validate coordinates and resolve them once."""
        lat = Decimal(str(latitude))
        lon = Decimal(str(longitude))

        if not Decimal("-90") <= lat <= Decimal("90"):
            raise InvalidCoordinatesError("Latitude must be between -90 and 90.")
        if not Decimal("-180") <= lon <= Decimal("180"):
            raise InvalidCoordinatesError("Longitude must be between -180 and 180.")

        raw = self.geocoding_service.reverse(
            latitude=float(lat),
            longitude=float(lon),
        )
        result = normalize_reverse_geocode(
            latitude=float(lat),
            longitude=float(lon),
            accuracy_meters=accuracy_meters,
            raw=raw,
        )
        reference = resolve_reference_entities(
            country_code=result["country_code"],
            state=result["state"],
            city=result["city"],
        )
        result["reference"] = reference
        result["timezone"] = reference.get("timezone", "")
        return result


__all__ = ("CurrentLocationService",)
