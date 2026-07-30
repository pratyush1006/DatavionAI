"""
URL patterns for the Payment Posting module.
"""

from __future__ import annotations

from apps.revenue_cycle.payment_posting.api.views import (
    PaymentPostingListCreateAPIView,
    PaymentPostingRetrieveUpdateDestroyAPIView,
)
from django.urls import path

app_name = "payment_postings"

urlpatterns = [
    path(
        "",
        PaymentPostingListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:posting_id>/",
        PaymentPostingRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
