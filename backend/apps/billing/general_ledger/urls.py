"""
General Ledger API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.billing.general_ledger.api.views import (
    GeneralLedgerAccountListCreateAPIView,
    GeneralLedgerAccountRetrieveUpdateDestroyAPIView,
)

app_name = "general_ledger"

urlpatterns = [
    path(
        "",
        GeneralLedgerAccountListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:account_id>/",
        GeneralLedgerAccountRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
