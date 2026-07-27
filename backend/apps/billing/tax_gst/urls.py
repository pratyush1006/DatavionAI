"""
Tax and GST URL patterns.
"""

from __future__ import annotations

from apps.billing.tax_gst.api.urls import urlpatterns

app_name = "tax_gst"

__all__ = [
    "app_name",
    "urlpatterns",
]
