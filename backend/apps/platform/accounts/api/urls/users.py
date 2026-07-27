"""
User management API routes.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.accounts.api.views import (
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
)

app_name = "users"


urlpatterns = [
    path(
        "",
        UserListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:user_id>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]
