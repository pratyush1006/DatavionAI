"""
Role Permission API URLs.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.rbac.api.role_permission.views import (
    RolePermissionListCreateAPIView,
    RolePermissionRetrieveUpdateDestroyAPIView,
)

app_name = "role-permissions"

urlpatterns = [
    path(
        "",
        RolePermissionListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:id>/",
        RolePermissionRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
