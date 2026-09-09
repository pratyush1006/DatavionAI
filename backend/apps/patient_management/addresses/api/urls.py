"""
URL configuration for Patient Addresses.
"""

from django.urls import path

from apps.patient_management.addresses.api.views import (
    AddressActivateAPIView,
    AddressDeactivateAPIView,
    AddressListCreateAPIView,
    AddressRetrieveUpdateDestroyAPIView,
    AddressSetPrimaryAPIView,
    AddressVerifyAPIView,
)

app_name = "patient-addresses"


urlpatterns = (
    path(
        "",
        AddressListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:address_id>/",
        AddressRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:address_id>/verify/",
        AddressVerifyAPIView.as_view(),
        name="verify",
    ),
    path(
        "<uuid:address_id>/activate/",
        AddressActivateAPIView.as_view(),
        name="activate",
    ),
    path(
        "<uuid:address_id>/deactivate/",
        AddressDeactivateAPIView.as_view(),
        name="deactivate",
    ),
    path(
        "<uuid:address_id>/set-primary/",
        AddressSetPrimaryAPIView.as_view(),
        name="set-primary",
    ),
)


__all__ = ("urlpatterns",)
