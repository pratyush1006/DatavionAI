"""
URL patterns for the Insurance Verification module.
"""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.insurance_verification.api.views import (
    InsuranceVerificationListCreateAPIView,
    InsuranceVerificationRetrieveUpdateDestroyAPIView,
)

app_name = "insurance_verifications"

urlpatterns = [
    path(
        "",
        InsuranceVerificationListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:verification_id>/",
        InsuranceVerificationRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
