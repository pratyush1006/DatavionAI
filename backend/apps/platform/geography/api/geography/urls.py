"""Geography API routes."""

from __future__ import annotations

from django.urls import path

from apps.platform.geography.api.geography.views.cities import CityListAPIView
from apps.platform.geography.api.geography.views.countries import CountryListAPIView
from apps.platform.geography.api.geography.views.current_location import (
    CurrentLocationAPIView,
)
from apps.platform.geography.api.geography.views.regions import RegionListAPIView
from apps.platform.geography.api.geography.views.tracking import (
    TrackingSessionCreateAPIView,
    TrackingSessionDetailAPIView,
    TrackingSessionLocationsAPIView,
    TrackingSessionParticipantAPIView,
    TrackingSessionStopAPIView,
)

app_name = "geography"
urlpatterns = [
    path("countries/", CountryListAPIView.as_view(), name="countries"),
    path("regions/", RegionListAPIView.as_view(), name="regions"),
    path("cities/", CityListAPIView.as_view(), name="cities"),
    path(
        "current-location/", CurrentLocationAPIView.as_view(), name="current-location"
    ),
    path(
        "tracking/sessions/",
        TrackingSessionCreateAPIView.as_view(),
        name="tracking-session-create",
    ),
    path(
        "tracking/sessions/<uuid:session_id>/",
        TrackingSessionDetailAPIView.as_view(),
        name="tracking-session-detail",
    ),
    path(
        "tracking/sessions/<uuid:session_id>/participants/",
        TrackingSessionParticipantAPIView.as_view(),
        name="tracking-session-participant",
    ),
    path(
        "tracking/sessions/<uuid:session_id>/stop/",
        TrackingSessionStopAPIView.as_view(),
        name="tracking-session-stop",
    ),
    path(
        "tracking/sessions/<uuid:session_id>/locations/",
        TrackingSessionLocationsAPIView.as_view(),
        name="tracking-session-locations",
    ),
]
