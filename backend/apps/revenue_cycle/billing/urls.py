"""
URL patterns for the Billing Batch module.
"""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.billing.api.views import (
    BillingBatchListCreateAPIView,
    BillingBatchRetrieveUpdateDestroyAPIView,
)

app_name = "billing_batches"

urlpatterns = [
    path(
        "",
        BillingBatchListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:batch_id>/",
        BillingBatchRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
