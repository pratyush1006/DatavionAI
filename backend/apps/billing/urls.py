"""
Billing API URL patterns.
"""

from __future__ import annotations

from django.urls import include, path

app_name = "billing"

urlpatterns = [
    path(
        "billing/",
        include(
            "apps.billing.api.urls",
        ),
    ),
    path(
        "billing/general-ledger/",
        include(
            "apps.billing.general_ledger.urls",
        ),
    ),
    path(
        "billing/accounts-payable/",
        include(
            "apps.billing.accounts_payable.urls",
        ),
    ),
    path(
        "billing/accounts-receivable/",
        include(
            "apps.billing.accounts_receivable.urls",
        ),
    ),
    path(
        "billing/cash-management/",
        include(
            "apps.billing.cash_management.urls",
        ),
    ),
    path(
        "billing/tax-gst/",
        include(
            "apps.billing.tax_gst.urls",
        ),
    ),
    path(
        "billing/financial-management/",
        include(
            "apps.billing.financial_management.urls",
        ),
    ),
]

__all__ = [
    "urlpatterns",
]
