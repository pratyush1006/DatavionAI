"""
URL patterns for the Portal Account module.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.portal.api.views import (
    PatientPortalAccountListCreateAPIView,
    PatientPortalAccountRetrieveUpdateDestroyAPIView,
)

app_name = "portal_accounts"

urlpatterns = [
    path(
        "",
        PatientPortalAccountListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:portal_account_id>/",
        PatientPortalAccountRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
