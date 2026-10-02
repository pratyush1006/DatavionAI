"""
Normalization of provider-specific reverse-geocoding responses.
"""

from __future__ import annotations


def normalize_reverse_geocode(
    *,
    latitude: float,
    longitude: float,
    accuracy_meters: float | None,
    raw: dict,
) -> dict:
    """Map provider fields into the DatavionOS geographic response contract."""
    address = raw.get("address") or {}
    city = (
        address.get("city")
        or address.get("town")
        or address.get("village")
        or address.get("municipality")
        or ""
    )
    state = address.get("state") or address.get("province") or ""
    district = (
        address.get("state_district")
        or address.get("district")
        or address.get("county")
        or ""
    )

    return {
        "latitude": float(raw.get("latitude", latitude)),
        "longitude": float(raw.get("longitude", longitude)),
        "accuracy_meters": accuracy_meters,
        "formatted_address": str(raw.get("display_name") or ""),
        "country": str(address.get("country") or ""),
        "country_code": str(address.get("country_code") or "").upper(),
        "state": str(state),
        "district": str(district),
        "city": str(city),
        "postal_code": str(address.get("postcode") or ""),
        "provider": str(raw.get("provider") or "unknown"),
    }


__all__ = ("normalize_reverse_geocode",)
