"""
URL configuration for Organization Domain APIs.
"""

from __future__ import annotations

from django.urls import path

from .views import (
    OrganizationDomainListCreateAPIView,
    OrganizationDomainRetrieveUpdateDestroyAPIView,
)

app_name = "organization-domain-api"

urlpatterns = [
    path(
        "",
        OrganizationDomainListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:pk>/",
        OrganizationDomainRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
]
