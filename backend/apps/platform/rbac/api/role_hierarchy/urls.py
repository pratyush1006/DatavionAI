"""
Role hierarchy API URLs.
"""

from __future__ import annotations

from django.urls import path

from .views import (
    RoleHierarchyDetailAPIView,
    RoleHierarchyListCreateAPIView,
)

app_name = "role-hierarchy-api"

urlpatterns = [
    path(
        "",
        RoleHierarchyListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<int:pk>/",
        RoleHierarchyDetailAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
