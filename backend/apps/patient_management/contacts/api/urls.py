"""
URL configuration for the Patient Contacts API.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.contacts.api.views import (
    ContactActivateAPIView,
    ContactDeactivateAPIView,
    ContactListCreateAPIView,
    ContactRetrieveUpdateDestroyAPIView,
    ContactSetPrimaryAPIView,
    ContactVerifyAPIView,
)

app_name = "patient-contacts"


urlpatterns = [
    path(
        "",
        ContactListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:contact_id>/",
        ContactRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:contact_id>/verify/",
        ContactVerifyAPIView.as_view(),
        name="verify",
    ),
    path(
        "<uuid:contact_id>/activate/",
        ContactActivateAPIView.as_view(),
        name="activate",
    ),
    path(
        "<uuid:contact_id>/deactivate/",
        ContactDeactivateAPIView.as_view(),
        name="deactivate",
    ),
    path(
        "<uuid:contact_id>/set-primary/",
        ContactSetPrimaryAPIView.as_view(),
        name="set-primary",
    ),
]


__all__ = ("urlpatterns",)
