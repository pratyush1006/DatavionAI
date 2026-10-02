"""
Reverse-geocoding workflow.
"""

from __future__ import annotations

from apps.platform.geography.services.geocoding import ReverseGeocodingService


def reverse_geocode_coordinates(*, latitude: float, longitude: float) -> dict:
    """Reverse-geocode a single coordinate pair."""
    return ReverseGeocodingService().reverse(
        latitude=latitude,
        longitude=longitude,
    )


__all__ = ("reverse_geocode_coordinates",)
