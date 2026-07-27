"""
Accounts Receivable URL patterns.
"""

from __future__ import annotations

from apps.billing.accounts_receivable.api.urls import urlpatterns

app_name = "accounts_receivable"

__all__ = [
    "app_name",
    "urlpatterns",
]
