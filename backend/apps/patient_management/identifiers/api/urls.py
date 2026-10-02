"""
Patient Identifier API routes.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.identifiers.api.views import (
    PatientIdentifierActivateAPIView,
    PatientIdentifierDeactivateAPIView,
    PatientIdentifierListCreateAPIView,
    PatientIdentifierRetrieveUpdateDestroyAPIView,
    PatientIdentifierRevokeAPIView,
    PatientIdentifierSetPrimaryAPIView,
    PatientIdentifierVerifyAPIView,
)

app_name = "patient-identifiers"


urlpatterns = [
    path(
        "",
        PatientIdentifierListCreateAPIView.as_view(),
        name="identifier-list-create",
    ),
    path(
        "<uuid:identifier_id>/",
        PatientIdentifierRetrieveUpdateDestroyAPIView.as_view(),
        name="identifier-detail",
    ),
    path(
        "<uuid:identifier_id>/verify/",
        PatientIdentifierVerifyAPIView.as_view(),
        name="identifier-verify",
    ),
    path(
        "<uuid:identifier_id>/activate/",
        PatientIdentifierActivateAPIView.as_view(),
        name="identifier-activate",
    ),
    path(
        "<uuid:identifier_id>/deactivate/",
        PatientIdentifierDeactivateAPIView.as_view(),
        name="identifier-deactivate",
    ),
    path(
        "<uuid:identifier_id>/revoke/",
        PatientIdentifierRevokeAPIView.as_view(),
        name="identifier-revoke",
    ),
    path(
        "<uuid:identifier_id>/set-primary/",
        PatientIdentifierSetPrimaryAPIView.as_view(),
        name="identifier-set-primary",
    ),
]


__all__ = ("urlpatterns",)
