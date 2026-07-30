"""
Role API URLs.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.rbac.api.role.views import (
    RoleListCreateAPIView,
    RoleRetrieveUpdateDestroyAPIView,
)

app_name = "roles"

urlpatterns = [
    path(
        "",
        RoleListCreateAPIView.as_view(),
        name="role-list",
    ),
    path(
        "<uuid:id>/",
        RoleRetrieveUpdateDestroyAPIView.as_view(),
        name="role-detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
