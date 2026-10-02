"""
Unit tests for current-location validation and normalization.
"""

from __future__ import annotations

from unittest.mock import Mock

import pytest

from apps.platform.geography.exceptions import InvalidCoordinatesError
from apps.platform.geography.services.current_location import CurrentLocationService


@pytest.mark.django_db
def test_current_location_resolves_once():
    """A supplied coordinate pair is normalized through the service boundary."""
    geocoder = Mock()
    geocoder.reverse.return_value = {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "display_name": "Bengaluru, Karnataka, India",
        "provider": "nominatim",
        "address": {
            "country": "India",
            "country_code": "in",
            "state": "Karnataka",
            "state_district": "Bengaluru Urban",
            "city": "Bengaluru",
            "postcode": "560001",
        },
    }

    result = CurrentLocationService(geocoding_service=geocoder).resolve(
        latitude=12.9716,
        longitude=77.5946,
        accuracy_meters=20,
    )

    assert result["country_code"] == "IN"
    assert result["state"] == "Karnataka"
    assert result["city"] == "Bengaluru"
    assert result["postal_code"] == "560001"
    assert result["provider"] == "nominatim"
    geocoder.reverse.assert_called_once()


@pytest.mark.parametrize(
    ("latitude", "longitude"),
    [(91, 0), (-91, 0), (0, 181), (0, -181)],
)
def test_invalid_coordinates_are_rejected(latitude, longitude):
    """Out-of-range Earth coordinates are rejected before provider access."""
    geocoder = Mock()
    with pytest.raises(InvalidCoordinatesError):
        CurrentLocationService(geocoding_service=geocoder).resolve(
            latitude=latitude,
            longitude=longitude,
        )
    geocoder.reverse.assert_not_called()
