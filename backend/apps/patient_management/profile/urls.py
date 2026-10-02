"""
URL patterns for the Patient Profile module.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.profile.api.views import (
    ProfileListCreateAPIView,
    ProfileRetrieveUpdateDestroyAPIView,
)

app_name = "patient_profile"

urlpatterns = [
    path(
        "",
        ProfileListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:profile_id>/",
        ProfileRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
