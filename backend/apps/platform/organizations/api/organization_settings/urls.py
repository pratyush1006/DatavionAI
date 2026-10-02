"""
URL configuration for OrganizationSettings API.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.organizations.api.organization_settings.views import (
    OrganizationSettingsListCreateAPIView,
    OrganizationSettingsRetrieveUpdateDestroyAPIView,
)

app_name = "organization-settings-api"

urlpatterns = (
    path(
        "",
        OrganizationSettingsListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:settings_id>/",
        OrganizationSettingsRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
)

__all__: tuple[str, ...] = (
    "app_name",
    "urlpatterns",
)
