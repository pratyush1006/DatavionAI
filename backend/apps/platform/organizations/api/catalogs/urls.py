"""
Organization catalog URL configuration.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.organizations.api.catalogs.views import (
    OrganizationCategoryCatalogAPIView,
    OrganizationSizeCatalogAPIView,
    OrganizationTypeCatalogAPIView,
)

app_name = "organization-catalogs"

urlpatterns = [
    path(
        "types/",
        OrganizationTypeCatalogAPIView.as_view(),
        name="types",
    ),
    path(
        "categories/",
        OrganizationCategoryCatalogAPIView.as_view(),
        name="categories",
    ),
    path(
        "sizes/",
        OrganizationSizeCatalogAPIView.as_view(),
        name="sizes",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
