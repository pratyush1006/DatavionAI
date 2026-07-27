"""
URLs for the Organization Module API.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.organizations.api.organization_module.views import (
    OrganizationModuleListCreateAPIView,
    OrganizationModuleRetrieveUpdateDestroyAPIView,
)

app_name = "organization-module-api"

urlpatterns = [
    path(
        "",
        OrganizationModuleListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:pk>/",
        OrganizationModuleRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
