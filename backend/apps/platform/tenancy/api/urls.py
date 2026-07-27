"""
Tenant API URL configuration.
"""

from __future__ import annotations

from django.urls import path

from apps.platform.tenancy.api.views import (
    MyTenantListAPIView,
    TenantCreateAPIView,
    TenantDetailAPIView,
    TenantListAPIView,
    TenantSelectAPIView,
)

app_name = "tenancy"


urlpatterns = [
    path(
        "tenants/",
        TenantListAPIView.as_view(),
        name="tenant-list",
    ),
    path(
        "tenants/create/",
        TenantCreateAPIView.as_view(),
        name="tenant-create",
    ),
    path(
        "tenants/<uuid:tenant_id>/",
        TenantDetailAPIView.as_view(),
        name="tenant-detail",
    ),
    path(
        "my-tenants/",
        MyTenantListAPIView.as_view(),
        name="my-tenants",
    ),
    path(
        "select/",
        TenantSelectAPIView.as_view(),
        name="tenant-select",
    ),
]


__all__ = (
    "app_name",
    "urlpatterns",
)
