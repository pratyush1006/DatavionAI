"""
Provider-independent reverse-geocoding service.
"""

from __future__ import annotations

from apps.platform.geography.providers.nominatim import NominatimProvider


class ReverseGeocodingService:
    """Resolve coordinates through the Geography provider boundary."""

    def __init__(self, provider=None) -> None:
        self.provider = provider or NominatimProvider()

    def reverse(self, *, latitude: float, longitude: float) -> dict:
        """Reverse-geocode one coordinate pair."""
        return self.provider.reverse(latitude=latitude, longitude=longitude)


__all__ = ("ReverseGeocodingService",)
