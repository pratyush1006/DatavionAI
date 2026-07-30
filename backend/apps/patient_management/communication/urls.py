"""
URL patterns for the Communication module.
"""

from __future__ import annotations

from apps.patient_management.communication.api.views import (
    PatientCommunicationListCreateAPIView,
    PatientCommunicationRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "communications"

urlpatterns = [
    path(
        "",
        PatientCommunicationListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:communication_id>/",
        PatientCommunicationRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
