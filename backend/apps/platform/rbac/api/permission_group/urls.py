"""
PermissionGroup API URLs.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.rbac.api.permission_group.views import (
    PermissionGroupListCreateAPIView,
    PermissionGroupRetrieveUpdateDestroyAPIView,
)

app_name = "permission-groups"

urlpatterns = [
    path(
        "",
        PermissionGroupListCreateAPIView.as_view(),
        name="permission-group-list",
    ),
    path(
        "<uuid:uuid>/",
        PermissionGroupRetrieveUpdateDestroyAPIView.as_view(),
        name="permission-group-detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
