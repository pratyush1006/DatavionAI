"""
Financial Management URL patterns.
"""

from __future__ import annotations

from apps.billing.financial_management.api.urls import urlpatterns

app_name = "financial_management"

__all__ = [
    "app_name",
    "urlpatterns",
]
