"""
Tax and GST API URL patterns.
"""

from __future__ import annotations

from apps.billing.tax_gst.api.views import (
    TaxFilingListCreateAPIView,
    TaxFilingRetrieveUpdateDestroyAPIView,
    TaxRateListCreateAPIView,
    TaxRateRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "tax_gst"

urlpatterns = [
    path(
        "tax_rates/",
        TaxRateListCreateAPIView.as_view(),
        name="tax_rate-list-create",
    ),
    path(
        "tax_rates/<uuid:tax_rate_id>/",
        TaxRateRetrieveUpdateDestroyAPIView.as_view(),
        name="tax_rate-detail",
    ),
    path(
        "tax_filings/",
        TaxFilingListCreateAPIView.as_view(),
        name="tax_filing-list-create",
    ),
    path(
        "tax_filings/<uuid:tax_filing_id>/",
        TaxFilingRetrieveUpdateDestroyAPIView.as_view(),
        name="tax_filing-detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
