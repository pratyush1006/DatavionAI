"""
Patient Consent endpoint routes.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.consents.api.views import (
    PatientConsentGrantView,
    PatientConsentListCreateView,
    PatientConsentRestoreView,
    PatientConsentRetrieveUpdateDestroyView,
    PatientConsentRevokeView,
)

urlpatterns = [
    path(
        "",
        PatientConsentListCreateView.as_view(),
        name="consent-list-create",
    ),
    path(
        "<uuid:pk>/",
        PatientConsentRetrieveUpdateDestroyView.as_view(),
        name="consent-detail",
    ),
    path(
        "<uuid:pk>/grant/",
        PatientConsentGrantView.as_view(),
        name="consent-grant",
    ),
    path(
        "<uuid:pk>/revoke/",
        PatientConsentRevokeView.as_view(),
        name="consent-revoke",
    ),
    path(
        "<uuid:pk>/restore/",
        PatientConsentRestoreView.as_view(),
        name="consent-restore",
    ),
]

__all__ = ("urlpatterns",)
