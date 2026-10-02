"""
Nominatim provider adapter implemented through GeoPy.

This is infrastructure only. Domain and API code never imports GeoPy directly.
"""

from __future__ import annotations

from typing import Any

from geopy.geocoders import Nominatim

from apps.platform.geography.exceptions import GeocodingProviderError


class NominatimProvider:
    """Reverse-geocode coordinates using Nominatim through GeoPy."""

    provider_name = "nominatim"

    def __init__(self, *, user_agent: str = "datavionos-geography") -> None:
        self._client = Nominatim(user_agent=user_agent, timeout=8)

    def reverse(self, *, latitude: float, longitude: float) -> dict[str, Any]:
        """Return provider-neutral raw geographic data."""
        try:
            location = self._client.reverse(
                (latitude, longitude),
                exactly_one=True,
                language="en",
            )
        except Exception as exc:
            raise GeocodingProviderError("Nominatim reverse geocoding failed.") from exc

        if location is None:
            raise GeocodingProviderError(
                "No geographic result was returned for the coordinates."
            )

        return {
            "latitude": float(location.latitude),
            "longitude": float(location.longitude),
            "display_name": str(location.address or ""),
            "address": dict(location.raw.get("address") or {}),
            "provider": self.provider_name,
        }


__all__ = ("NominatimProvider",)
