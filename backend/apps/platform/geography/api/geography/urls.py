"""
Geography API URL configuration.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.geography.api.geography.views import (
    CityListAPIView,
    CountryListAPIView,
    RegionListAPIView,
)

app_name = "geography"


urlpatterns = (
    path(
        "countries/",
        CountryListAPIView.as_view(),
        name="countries",
    ),
    path(
        "regions/",
        RegionListAPIView.as_view(),
        name="regions",
    ),
    path(
        "cities/",
        CityListAPIView.as_view(),
        name="cities",
    ),
)


__all__: tuple[str, ...] = (
    "app_name",
    "urlpatterns",
)
