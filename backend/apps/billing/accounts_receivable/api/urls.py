"""
Accounts Receivable API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.billing.accounts_receivable.api.views import (
    CustomerInvoiceListCreateAPIView,
    CustomerInvoiceRetrieveUpdateDestroyAPIView,
    CustomerListCreateAPIView,
    CustomerRetrieveUpdateDestroyAPIView,
)

app_name = "accounts_receivable"

urlpatterns = [
    path(
        "customers/",
        CustomerListCreateAPIView.as_view(),
        name="customer-list-create",
    ),
    path(
        "customers/<uuid:customer_id>/",
        CustomerRetrieveUpdateDestroyAPIView.as_view(),
        name="customer-detail",
    ),
    path(
        "customer_invoices/",
        CustomerInvoiceListCreateAPIView.as_view(),
        name="customer_invoice-list-create",
    ),
    path(
        "customer_invoices/<uuid:customer_invoice_id>/",
        CustomerInvoiceRetrieveUpdateDestroyAPIView.as_view(),
        name="customer_invoice-detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
