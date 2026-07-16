"""
Permission API URL configuration.
"""

from __future__ import annotations

from apps.platform.rbac.api.permission.views import (
    PermissionListCreateAPIView,
    PermissionRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "permissions"

urlpatterns = [
    path(
        "",
        PermissionListCreateAPIView.as_view(),
        name="permission-list",
    ),
    path(
        "<uuid:permission_id>/",
        PermissionRetrieveUpdateDestroyAPIView.as_view(),
        name="permission-detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
