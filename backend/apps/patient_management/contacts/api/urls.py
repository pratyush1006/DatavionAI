"""
URL configuration for the Contacts API.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.contacts.api.views import (
    ContactCreateAPIView,
    ContactDestroyAPIView,
    ContactListAPIView,
    ContactRetrieveAPIView,
    ContactUpdateAPIView,
)

app_name = "patient-contacts"

urlpatterns = [
    path(
        "",
        ContactListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        ContactCreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<uuid:pk>/",
        ContactRetrieveAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:pk>/update/",
        ContactUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:pk>/delete/",
        ContactDestroyAPIView.as_view(),
        name="delete",
    ),
]
