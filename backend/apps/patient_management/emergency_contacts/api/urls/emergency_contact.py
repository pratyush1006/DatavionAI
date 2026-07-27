"""
URL configuration for Emergency Contact APIs.
"""

from __future__ import annotations

from django.urls import path

from ..views import (
    EmergencyContactCreateAPIView,
    EmergencyContactDeleteAPIView,
    EmergencyContactListAPIView,
    EmergencyContactRetrieveAPIView,
    EmergencyContactUpdateAPIView,
)

app_name = "emergency-contacts"

urlpatterns = [
    path(
        "",
        EmergencyContactListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        EmergencyContactCreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<uuid:id>/",
        EmergencyContactRetrieveAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:id>/update/",
        EmergencyContactUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:id>/delete/",
        EmergencyContactDeleteAPIView.as_view(),
        name="delete",
    ),
]
