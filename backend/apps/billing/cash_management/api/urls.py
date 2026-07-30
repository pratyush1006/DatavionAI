"""
Cash Management API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.billing.cash_management.api.views import (
    BankAccountListCreateAPIView,
    BankAccountRetrieveUpdateDestroyAPIView,
    CashTransactionListCreateAPIView,
    CashTransactionRetrieveUpdateDestroyAPIView,
)

app_name = "cash_management"

urlpatterns = [
    path(
        "bank_accounts/",
        BankAccountListCreateAPIView.as_view(),
        name="bank_account-list-create",
    ),
    path(
        "bank_accounts/<uuid:bank_account_id>/",
        BankAccountRetrieveUpdateDestroyAPIView.as_view(),
        name="bank_account-detail",
    ),
    path(
        "cash_transactions/",
        CashTransactionListCreateAPIView.as_view(),
        name="cash_transaction-list-create",
    ),
    path(
        "cash_transactions/<uuid:cash_transaction_id>/",
        CashTransactionRetrieveUpdateDestroyAPIView.as_view(),
        name="cash_transaction-detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
