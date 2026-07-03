"""
API URL configuration for the Accounts application.
"""

from __future__ import annotations

from django.urls import path

from apps.accounts.api.views import (
    LoginAPIView,
    MeAPIView,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "login/",
        LoginAPIView.as_view(),
        name="login",
    ),
    path(
        "me/",
        MeAPIView.as_view(),
        name="me",
    ),
    path(
        "",
        UserListCreateAPIView.as_view(),
        name="user-list-create",
    ),
    path(
        "<int:user_id>/",
        UserRetrieveUpdateDestroyAPIView.as_view(),
        name="user-detail",
    ),
]

__all__ = [
    "urlpatterns",
]
