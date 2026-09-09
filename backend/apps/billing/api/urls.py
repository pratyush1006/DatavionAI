"""
Billing Core API URLs.
"""

from __future__ import annotations

from django.urls import path

from apps.billing.api.views import (
    InsuranceClaimAppealAPIView,
    InsuranceClaimApproveAPIView,
    InsuranceClaimListCreateAPIView,
    InsuranceClaimRejectAPIView,
    InsuranceClaimRetrieveUpdateAPIView,
    InsuranceClaimSettleAPIView,
    InvoiceListCreateAPIView,
    InvoiceRetrieveUpdateDestroyAPIView,
    PaymentBulkCreateAPIView,
    PaymentListCreateAPIView,
    PaymentRetrieveAPIView,
)

app_name = "billing_api"

urlpatterns = (
    path("invoices/", InvoiceListCreateAPIView.as_view(), name="invoice-list-create"),
    path(
        "invoices/<uuid:invoice_id>/",
        InvoiceRetrieveUpdateDestroyAPIView.as_view(),
        name="invoice-detail",
    ),
    path("payments/", PaymentListCreateAPIView.as_view(), name="payment-list-create"),
    path(
        "payments/<uuid:payment_id>/",
        PaymentRetrieveAPIView.as_view(),
        name="payment-detail",
    ),
    path(
        "payments/bulk/", PaymentBulkCreateAPIView.as_view(), name="payment-bulk-create"
    ),
    path(
        "insurance-claims/",
        InsuranceClaimListCreateAPIView.as_view(),
        name="claim-list-create",
    ),
    path(
        "insurance-claims/<uuid:claim_id>/",
        InsuranceClaimRetrieveUpdateAPIView.as_view(),
        name="claim-detail",
    ),
    path(
        "insurance-claims/<uuid:claim_id>/approve/",
        InsuranceClaimApproveAPIView.as_view(),
        name="claim-approve",
    ),
    path(
        "insurance-claims/<uuid:claim_id>/reject/",
        InsuranceClaimRejectAPIView.as_view(),
        name="claim-reject",
    ),
    path(
        "insurance-claims/<uuid:claim_id>/appeal/",
        InsuranceClaimAppealAPIView.as_view(),
        name="claim-appeal",
    ),
    path(
        "insurance-claims/<uuid:claim_id>/settle/",
        InsuranceClaimSettleAPIView.as_view(),
        name="claim-settle",
    ),
)

__all__ = ("app_name", "urlpatterns")
