"""
End-to-end API contract tests for Geography.
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from rest_framework.test import APIRequestFactory

from apps.platform.geography.api.geography.views.current_location import (
    CurrentLocationAPIView,
)


@pytest.mark.django_db
def test_current_location_api_contract():
    """Coordinates travel through the API into the service and return the public contract."""
    factory = APIRequestFactory()
    payload = {"latitude": "12.971600", "longitude": "77.594600", "accuracy_meters": 20}
    resolved = {
        "latitude": 12.9716,
        "longitude": 77.5946,
        "accuracy_meters": 20.0,
        "formatted_address": "Bengaluru, Karnataka, India",
        "country": "India",
        "country_code": "IN",
        "state": "Karnataka",
        "district": "Bengaluru Urban",
        "city": "Bengaluru",
        "postal_code": "560001",
        "provider": "nominatim",
        "reference": {"country_id": None, "region_id": None, "city_id": None},
    }
    with patch.object(CurrentLocationAPIView, "permission_classes", ()):
        with patch(
            "apps.platform.geography.api.geography.views.current_location.CurrentLocationService.resolve",
            return_value=resolved,
        ):
            response = CurrentLocationAPIView.as_view()(
                factory.post("/api/geography/current-location/", payload, format="json")
            )
    assert response.status_code == 200
    assert response.data["country_code"] == "IN"
    assert response.data["reference"]["country_id"] is None


def test_current_location_api_rejects_invalid_coordinates():
    """Invalid coordinates fail at the serializer boundary."""
    factory = APIRequestFactory()
    response = CurrentLocationAPIView.as_view()(
        factory.post(
            "/api/geography/current-location/",
            {"latitude": 91, "longitude": 0},
            format="json",
        )
    )
    assert response.status_code == 400
