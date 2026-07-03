"""
Organization API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.organizations.api.views import (
    OrganizationListCreateAPIView,
    OrganizationRetrieveUpdateDestroyAPIView,
)

app_name = "organizations"

urlpatterns = [
    path(
        "",
        OrganizationListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<int:organization_id>/",
        OrganizationRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]
