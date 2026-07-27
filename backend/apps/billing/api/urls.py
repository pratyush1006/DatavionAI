"""
Billing API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.billing.api.views import (
    InsuranceClaimApproveAPIView,
    InsuranceClaimBulkCreateAPIView,
    InsuranceClaimListCreateAPIView,
    InsuranceClaimRejectAPIView,
    InsuranceClaimRetrieveUpdateAPIView,
    InvoiceBulkCreateAPIView,
    InvoiceListCreateAPIView,
    InvoiceRetrieveUpdateDestroyAPIView,
    InvoiceVoidAPIView,
    PaymentBulkCreateAPIView,
    PaymentListCreateAPIView,
    PaymentRetrieveAPIView,
)

app_name = "billing"

urlpatterns = [
    path(
        "invoices/",
        InvoiceListCreateAPIView.as_view(),
        name="invoice-list-create",
    ),
    path(
        "invoices/<uuid:invoice_id>/",
        InvoiceRetrieveUpdateDestroyAPIView.as_view(),
        name="invoice-detail",
    ),
    path(
        "invoices/<uuid:invoice_id>/items/",
        InvoiceListCreateAPIView.as_view(),
        name="invoice-items",
    ),
    path(
        "invoices/bulk/",
        InvoiceBulkCreateAPIView.as_view(),
        name="invoice-bulk-create",
    ),
    path(
        "invoices/<uuid:invoice_id>/void/",
        InvoiceVoidAPIView.as_view(),
        name="invoice-void",
    ),
    path(
        "payments/",
        PaymentListCreateAPIView.as_view(),
        name="payment-list-create",
    ),
    path(
        "payments/<uuid:payment_id>/",
        PaymentRetrieveAPIView.as_view(),
        name="payment-detail",
    ),
    path(
        "payments/bulk/",
        PaymentBulkCreateAPIView.as_view(),
        name="payment-bulk-create",
    ),
    path(
        "claims/",
        InsuranceClaimListCreateAPIView.as_view(),
        name="claim-list-create",
    ),
    path(
        "claims/<uuid:claim_id>/",
        InsuranceClaimRetrieveUpdateAPIView.as_view(),
        name="claim-detail",
    ),
    path(
        "claims/bulk/",
        InsuranceClaimBulkCreateAPIView.as_view(),
        name="claim-bulk-create",
    ),
    path(
        "claims/<uuid:claim_id>/approve/",
        InsuranceClaimApproveAPIView.as_view(),
        name="claim-approve",
    ),
    path(
        "claims/<uuid:claim_id>/reject/",
        InsuranceClaimRejectAPIView.as_view(),
        name="claim-reject",
    ),
]


__all__ = [
    "urlpatterns",
]
