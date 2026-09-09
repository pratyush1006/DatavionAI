"""
URL configuration for the Patient Family Members module.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "family-members"


urlpatterns = (
    path(
        "",
        include(
            "apps.patient_management.family_members.api.urls.family_member",
        ),
    ),
)


__all__ = (
    "app_name",
    "urlpatterns",
)
