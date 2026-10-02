"""
User role API URLs.
"""

from __future__ import annotations

from django.urls import (
    path,
)

from apps.platform.rbac.api.user_role.views import (
    UserRoleListCreateAPIView,
    UserRoleRetrieveUpdateDestroyAPIView,
)

app_name = "user-role-api"

urlpatterns = [
    path(
        "",
        UserRoleListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:id>/",
        UserRoleRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]


__all__ = [
    "urlpatterns",
]
