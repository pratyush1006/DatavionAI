"""
Organization API URL configuration.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization.views import (
    OrganizationListCreateAPIView,
    OrganizationRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "organizations"

urlpatterns = (
    path(
        "",
        OrganizationListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:organization_id>/",
        OrganizationRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
)

__all__: tuple[str, ...] = (
    "app_name",
    "urlpatterns",
)
