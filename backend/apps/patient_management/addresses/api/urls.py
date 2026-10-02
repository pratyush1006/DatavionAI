"""Patient Address API routes."""

from __future__ import annotations

from django.urls import path

from apps.patient_management.addresses.api.views import (
    AddressDetailAPIView,
    AddressListCreateAPIView,
    AddressReverseGeocodeAPIView,
    AddressVerifyAPIView,
)

app_name = "patient-management-addresses"
urlpatterns = [
    path("", AddressListCreateAPIView.as_view(), name="address-list-create"),
    path("<uuid:address_id>/", AddressDetailAPIView.as_view(), name="address-detail"),
    path(
        "<uuid:address_id>/verify/",
        AddressVerifyAPIView.as_view(),
        name="address-verify",
    ),
    path(
        "<uuid:address_id>/reverse-geocode/",
        AddressReverseGeocodeAPIView.as_view(),
        name="address-reverse-geocode",
    ),
]
