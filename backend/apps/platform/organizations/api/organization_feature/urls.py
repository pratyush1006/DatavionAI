"""
URL configuration for Organization Feature APIs.
"""

from __future__ import annotations

from django.urls import path

from .views import (
    OrganizationFeatureListCreateAPIView,
    OrganizationFeatureRetrieveUpdateDestroyAPIView,
)

app_name = "organization-feature-api"

urlpatterns = [
    path(
        "",
        OrganizationFeatureListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:pk>/",
        OrganizationFeatureRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
]
