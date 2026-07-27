"""
Accounts Payable URL patterns.
"""

from __future__ import annotations

from apps.billing.accounts_payable.api.urls import urlpatterns

app_name = "accounts_payable"

__all__ = [
    "app_name",
    "urlpatterns",
]
