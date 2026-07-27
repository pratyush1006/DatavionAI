"""
Organization Hierarchy API URL configuration.
"""

from __future__ import annotations

from apps.platform.organizations.api.organization_hierarchy.views import (
    OrganizationHierarchyListCreateAPIView,
    OrganizationHierarchyRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "organization-hierarchy-api"

urlpatterns = [
    path(
        "",
        OrganizationHierarchyListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:hierarchy_id>/",
        OrganizationHierarchyRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
]

__all__: tuple[str, ...] = (
    "app_name",
    "urlpatterns",
)
