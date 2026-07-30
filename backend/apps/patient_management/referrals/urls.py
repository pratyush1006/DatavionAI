"""
URL patterns for the Referral module.
"""

from __future__ import annotations

from apps.patient_management.referrals.api.views import (
    PatientReferralListCreateAPIView,
    PatientReferralRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "referrals_rec"

urlpatterns = [
    path(
        "",
        PatientReferralListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:referral_id>/",
        PatientReferralRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
