"""Revenue Cycle Insurance Verification URL routes."""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.insurance_verification.api.views import (
    InsuranceVerificationDetailAPIView,
    InsuranceVerificationLifecycleAPIView,
    InsuranceVerificationListCreateAPIView,
    InsuranceVerificationRestoreAPIView,
)

app_name = "revenue_cycle_insurance_verification"

urlpatterns = (
    path("", InsuranceVerificationListCreateAPIView.as_view(), name="list-create"),
    path(
        "<uuid:verification_id>/",
        InsuranceVerificationDetailAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:verification_id>/lifecycle/",
        InsuranceVerificationLifecycleAPIView.as_view(),
        name="lifecycle",
    ),
    path(
        "<uuid:verification_id>/restore/",
        InsuranceVerificationRestoreAPIView.as_view(),
        name="restore",
    ),
)

__all__ = ("app_name", "urlpatterns")
