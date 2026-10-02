"""Compliance URL configuration."""

from django.urls import path

from apps.compliance.api.views import (
    ConsentDetailAPIView,
    ConsentListCreateAPIView,
    PhiAccessLogListAPIView,
)

urlpatterns = [
    path("consents/", ConsentListCreateAPIView.as_view(), name="consent-list-create"),
    path(
        "consents/<uuid:consent_id>/",
        ConsentDetailAPIView.as_view(),
        name="consent-detail",
    ),
    path(
        "phi-access-logs/",
        PhiAccessLogListAPIView.as_view(),
        name="phi-access-log-list",
    ),
]
