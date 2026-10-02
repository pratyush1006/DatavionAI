"""
Organization role API URLs.
"""

from __future__ import annotations

from django.urls import path

from .views import (
    OrganizationRoleDetailAPIView,
    OrganizationRoleListCreateAPIView,
)

app_name = "organization-role-api"

urlpatterns = [
    path(
        "",
        OrganizationRoleListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<int:pk>/",
        OrganizationRoleDetailAPIView.as_view(),
        name="detail",
    ),
]
