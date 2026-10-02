"""URL routes for Revenue Cycle Accounts Receivable."""

from __future__ import annotations

from django.urls import path

from .api.views import (
    ARAccountHoldAPIView,
    ARAccountHoldReleaseAPIView,
    ARAccountListAPIView,
    ARAccountWriteOffAPIView,
    ARTransactionListCreateAPIView,
    ARTransactionReverseAPIView,
)

app_name = "revenue_cycle_accounts_receivable"

urlpatterns = [
    path(
        "accounts/",
        ARAccountListAPIView.as_view(),
        name="account-list",
    ),
    path(
        "accounts/<uuid:account_id>/transactions/",
        ARTransactionListCreateAPIView.as_view(),
        name="transaction-list-create",
    ),
    path(
        "transactions/<uuid:transaction_id>/reverse/",
        ARTransactionReverseAPIView.as_view(),
        name="transaction-reverse",
    ),
    path(
        "accounts/<uuid:account_id>/hold/",
        ARAccountHoldAPIView.as_view(),
        name="account-hold",
    ),
    path(
        "accounts/<uuid:account_id>/release-hold/",
        ARAccountHoldReleaseAPIView.as_view(),
        name="account-release-hold",
    ),
    path(
        "accounts/<uuid:account_id>/write-off/",
        ARAccountWriteOffAPIView.as_view(),
        name="account-write-off",
    ),
]

__all__ = ("app_name", "urlpatterns")
