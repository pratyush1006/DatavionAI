"""
Accounts Receivable URL patterns.
"""

from __future__ import annotations

from apps.revenue_cycle.billing.accounts_receivable.api.urls import urlpatterns

app_name = "accounts_receivable"

__all__ = [
    "app_name",
    "urlpatterns",
]
