"""
Patient Registration API routes.
"""

from __future__ import annotations

from apps.patient_management.registration.api.views import (
    PatientRegistrationCancelAPIView,
    PatientRegistrationCheckInAPIView,
    PatientRegistrationCompleteAPIView,
    PatientRegistrationListCreateAPIView,
    PatientRegistrationNoShowAPIView,
    PatientRegistrationRejectAPIView,
    PatientRegistrationRetrieveUpdateDestroyAPIView,
    PatientRegistrationVerifyAPIView,
)
from django.urls import path

app_name = "patient-registrations"


urlpatterns = [
    path(
        "",
        PatientRegistrationListCreateAPIView.as_view(),
        name="registration-list-create",
    ),
    path(
        "<uuid:registration_id>/",
        PatientRegistrationRetrieveUpdateDestroyAPIView.as_view(),
        name="registration-detail",
    ),
    path(
        "<uuid:registration_id>/verify/",
        PatientRegistrationVerifyAPIView.as_view(),
        name="registration-verify",
    ),
    path(
        "<uuid:registration_id>/check-in/",
        PatientRegistrationCheckInAPIView.as_view(),
        name="registration-check-in",
    ),
    path(
        "<uuid:registration_id>/complete/",
        PatientRegistrationCompleteAPIView.as_view(),
        name="registration-complete",
    ),
    path(
        "<uuid:registration_id>/cancel/",
        PatientRegistrationCancelAPIView.as_view(),
        name="registration-cancel",
    ),
    path(
        "<uuid:registration_id>/reject/",
        PatientRegistrationRejectAPIView.as_view(),
        name="registration-reject",
    ),
    path(
        "<uuid:registration_id>/no-show/",
        PatientRegistrationNoShowAPIView.as_view(),
        name="registration-no-show",
    ),
]


__all__ = ("urlpatterns",)
