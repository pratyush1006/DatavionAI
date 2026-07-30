"""
DatavionOS SaaS Billing API URLs.

Routes:

- Billing Account
- Subscription
- Invoice
- Payment
- Usage
"""

from __future__ import annotations

from django.urls import path

from apps.platform.saas_billing.api.views import (
    BillingAccountDetailAPIView,
    BillingAccountUpdateAPIView,
    BillingAutoChargeAPIView,
    BillingPaymentProviderAPIView,
    InvoiceCancelAPIView,
    InvoiceDetailAPIView,
    InvoiceFinalizeAPIView,
    InvoiceGenerateAPIView,
    InvoiceIssueAPIView,
    InvoiceListAPIView,
    PaymentDetailAPIView,
    PaymentListAPIView,
    PaymentProcessAPIView,
    PaymentReconcileAPIView,
    PaymentRefundAPIView,
    SubscriptionActivateAPIView,
    SubscriptionCancelAPIView,
    SubscriptionCreateAPIView,
    SubscriptionDetailAPIView,
    SubscriptionRenewAPIView,
    UsageChargeAPIView,
    UsageCollectAPIView,
    UsageEvaluateAPIView,
    UsageListAPIView,
)

urlpatterns = [
    # =========================================================================
    # Billing Account
    # =========================================================================
    path(
        "account/",
        BillingAccountDetailAPIView.as_view(),
        name="billing-account-detail",
    ),
    path(
        "account/update/",
        BillingAccountUpdateAPIView.as_view(),
        name="billing-account-update",
    ),
    path(
        "account/payment-provider/",
        BillingPaymentProviderAPIView.as_view(),
        name="billing-payment-provider",
    ),
    path(
        "account/auto-charge/",
        BillingAutoChargeAPIView.as_view(),
        name="billing-auto-charge",
    ),
    # =========================================================================
    # Subscription
    # =========================================================================
    path(
        "subscription/",
        SubscriptionDetailAPIView.as_view(),
        name="subscription-detail",
    ),
    path(
        "subscription/create/",
        SubscriptionCreateAPIView.as_view(),
        name="subscription-create",
    ),
    path(
        "subscription/activate/",
        SubscriptionActivateAPIView.as_view(),
        name="subscription-activate",
    ),
    path(
        "subscription/renew/",
        SubscriptionRenewAPIView.as_view(),
        name="subscription-renew",
    ),
    path(
        "subscription/cancel/",
        SubscriptionCancelAPIView.as_view(),
        name="subscription-cancel",
    ),
    # =========================================================================
    # Invoice
    # =========================================================================
    path(
        "invoices/",
        InvoiceListAPIView.as_view(),
        name="invoice-list",
    ),
    path(
        "invoices/<uuid:pk>/",
        InvoiceDetailAPIView.as_view(),
        name="invoice-detail",
    ),
    path(
        "invoices/generate/",
        InvoiceGenerateAPIView.as_view(),
        name="invoice-generate",
    ),
    path(
        "invoices/<uuid:pk>/issue/",
        InvoiceIssueAPIView.as_view(),
        name="invoice-issue",
    ),
    path(
        "invoices/<uuid:pk>/finalize/",
        InvoiceFinalizeAPIView.as_view(),
        name="invoice-finalize",
    ),
    path(
        "invoices/<uuid:pk>/cancel/",
        InvoiceCancelAPIView.as_view(),
        name="invoice-cancel",
    ),
    # =========================================================================
    # Payment
    # =========================================================================
    path(
        "payments/",
        PaymentListAPIView.as_view(),
        name="payment-list",
    ),
    path(
        "payments/<uuid:pk>/",
        PaymentDetailAPIView.as_view(),
        name="payment-detail",
    ),
    path(
        "payments/process/",
        PaymentProcessAPIView.as_view(),
        name="payment-process",
    ),
    path(
        "payments/<uuid:pk>/reconcile/",
        PaymentReconcileAPIView.as_view(),
        name="payment-reconcile",
    ),
    path(
        "payments/<uuid:pk>/refund/",
        PaymentRefundAPIView.as_view(),
        name="payment-refund",
    ),
    # =========================================================================
    # Usage
    # =========================================================================
    path(
        "usage/",
        UsageListAPIView.as_view(),
        name="usage-list",
    ),
    path(
        "usage/collect/",
        UsageCollectAPIView.as_view(),
        name="usage-collect",
    ),
    path(
        "usage/<uuid:pk>/evaluate/",
        UsageEvaluateAPIView.as_view(),
        name="usage-evaluate",
    ),
    path(
        "usage/<uuid:pk>/charge/",
        UsageChargeAPIView.as_view(),
        name="usage-charge",
    ),
]
