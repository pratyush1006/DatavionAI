"""
URL configuration for the Addresses API.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.addresses.api.views import (
    AddressCreateAPIView,
    AddressDestroyAPIView,
    AddressListAPIView,
    AddressRetrieveAPIView,
    AddressUpdateAPIView,
)

app_name = "patient-addresses"

urlpatterns = [
    path(
        "",
        AddressListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        AddressCreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<uuid:pk>/",
        AddressRetrieveAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:pk>/update/",
        AddressUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:pk>/delete/",
        AddressDestroyAPIView.as_view(),
        name="delete",
    ),
]
