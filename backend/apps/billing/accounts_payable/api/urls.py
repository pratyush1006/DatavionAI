"""
Accounts Payable API URL patterns.
"""

from __future__ import annotations

from apps.billing.accounts_payable.api.views import (
    VendorInvoiceListCreateAPIView,
    VendorInvoiceRetrieveUpdateDestroyAPIView,
    VendorListCreateAPIView,
    VendorRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "accounts_payable"

urlpatterns = [
    path(
        "vendors/",
        VendorListCreateAPIView.as_view(),
        name="vendor-list-create",
    ),
    path(
        "vendors/<uuid:vendor_id>/",
        VendorRetrieveUpdateDestroyAPIView.as_view(),
        name="vendor-detail",
    ),
    path(
        "vendor_invoices/",
        VendorInvoiceListCreateAPIView.as_view(),
        name="vendor_invoice-list-create",
    ),
    path(
        "vendor_invoices/<uuid:vendor_invoice_id>/",
        VendorInvoiceRetrieveUpdateDestroyAPIView.as_view(),
        name="vendor_invoice-detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
