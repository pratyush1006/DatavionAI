"""URL configuration for payment posting."""

from __future__ import annotations

from django.urls import path

from .api.views import (
    PaymentPostingDetailAPIView,
    PaymentPostingListCreateAPIView,
    PaymentPostingPostAPIView,
    PaymentPostingRestoreAPIView,
    PaymentPostingReverseAPIView,
)

app_name = "revenue_cycle_payment_posting"

urlpatterns = (
    path("", PaymentPostingListCreateAPIView.as_view(), name="list-create"),
    path("<uuid:posting_id>/", PaymentPostingDetailAPIView.as_view(), name="detail"),
    path("<uuid:posting_id>/post/", PaymentPostingPostAPIView.as_view(), name="post"),
    path(
        "<uuid:posting_id>/reverse/",
        PaymentPostingReverseAPIView.as_view(),
        name="reverse",
    ),
    path(
        "<uuid:posting_id>/restore/",
        PaymentPostingRestoreAPIView.as_view(),
        name="restore",
    ),
)

__all__ = ("app_name", "urlpatterns")
