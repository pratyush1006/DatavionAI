"""
Organization Branding API URL configuration.
"""

from __future__ import annotations

from django.urls import (
    path,
)

from apps.platform.organizations.api.organization_branding.views import (
    OrganizationBrandingByOrganizationAPIView,
    OrganizationBrandingListCreateAPIView,
    OrganizationBrandingRetrieveUpdateDestroyAPIView,
)

app_name = "organization-branding"

urlpatterns = (
    path(
        "",
        OrganizationBrandingListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:branding_id>/",
        OrganizationBrandingRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path(
        "by-organization/<uuid:organization_id>/",
        OrganizationBrandingByOrganizationAPIView.as_view(),
        name="by-organization",
    ),
)

__all__: tuple[str, ...] = (
    "app_name",
    "urlpatterns",
)
