"""
URL routes for Patient Referrals.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.referrals.api.views import (
    PatientReferralDetailAPIView,
    PatientReferralListCreateAPIView,
    PatientReferralRestoreAPIView,
    PatientReferralTransitionAPIView,
)

app_name = "patient_referrals"

urlpatterns = [
    path(
        "",
        PatientReferralListCreateAPIView.as_view(),
        name="referral-list-create",
    ),
    path(
        "<uuid:pk>/",
        PatientReferralDetailAPIView.as_view(),
        name="referral-detail",
    ),
    path(
        "<uuid:pk>/transition/",
        PatientReferralTransitionAPIView.as_view(),
        name="referral-transition",
    ),
    path(
        "<uuid:pk>/restore/",
        PatientReferralRestoreAPIView.as_view(),
        name="referral-restore",
    ),
]

__all__ = (
    "app_name",
    "urlpatterns",
)
