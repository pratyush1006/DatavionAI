"""URL patterns for Patient Relationships API."""

from __future__ import annotations

from django.urls import path

from apps.patient_management.relationships.api.views import (
    PatientRelationshipActivateAPIView,
    PatientRelationshipDeactivateAPIView,
    PatientRelationshipListCreateAPIView,
    PatientRelationshipRestoreAPIView,
    PatientRelationshipRetrieveUpdateDestroyAPIView,
    PatientRelationshipSetPrimaryAPIView,
    PatientRelationshipTerminateAPIView,
    PatientRelationshipVerifyAPIView,
)

app_name = "patient-relationships"


urlpatterns = (
    path(
        "",
        PatientRelationshipListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:relationship_id>/",
        PatientRelationshipRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path(
        "<uuid:relationship_id>/activate/",
        PatientRelationshipActivateAPIView.as_view(),
        name="activate",
    ),
    path(
        "<uuid:relationship_id>/deactivate/",
        PatientRelationshipDeactivateAPIView.as_view(),
        name="deactivate",
    ),
    path(
        "<uuid:relationship_id>/restore/",
        PatientRelationshipRestoreAPIView.as_view(),
        name="restore",
    ),
    path(
        "<uuid:relationship_id>/verify/",
        PatientRelationshipVerifyAPIView.as_view(),
        name="verify",
    ),
    path(
        "<uuid:relationship_id>/terminate/",
        PatientRelationshipTerminateAPIView.as_view(),
        name="terminate",
    ),
    path(
        "<uuid:relationship_id>/set-primary/",
        PatientRelationshipSetPrimaryAPIView.as_view(),
        name="set-primary",
    ),
)


__all__ = (
    "app_name",
    "urlpatterns",
)
