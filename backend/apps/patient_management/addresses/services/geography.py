"""Patient Address -> Platform Geography integration boundary."""

from __future__ import annotations

from importlib import import_module

from apps.patient_management.addresses.exceptions import AddressGeographyError


def _find_service():
    candidates = (
        (
            "apps.platform.geography.services.reverse_geocoding",
            "ReverseGeocodingService",
        ),
        ("apps.platform.geography.services.geocoding", "ReverseGeocodingService"),
        ("apps.platform.geography.services", "ReverseGeocodingService"),
    )
    for module_name, class_name in candidates:
        try:
            return getattr(import_module(module_name), class_name)
        except (ImportError, AttributeError):
            continue
    raise AddressGeographyError(
        "Canonical Platform Geography ReverseGeocodingService is unavailable."
    )


def reverse_geocode(*, latitude: float, longitude: float):
    service = _find_service()()
    for name in ("reverse_geocode", "reverse", "resolve"):
        method = getattr(service, name, None)
        if method is not None:
            return method(latitude=latitude, longitude=longitude)
    raise AddressGeographyError(
        "Platform Geography reverse-geocoding service exposes no supported operation."
    )
