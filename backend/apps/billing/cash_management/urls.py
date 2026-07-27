"""
Cash Management URL patterns.
"""

from __future__ import annotations

from apps.billing.cash_management.api.urls import urlpatterns

app_name = "cash_management"

__all__ = [
    "app_name",
    "urlpatterns",
]
