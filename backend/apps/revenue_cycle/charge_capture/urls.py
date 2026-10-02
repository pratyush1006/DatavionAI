"""Root URL configuration for Revenue Cycle Charge Capture."""

from __future__ import annotations

from django.urls import include, path

__all__ = ("urlpatterns",)

urlpatterns = [
    path("", include("apps.revenue_cycle.charge_capture.api.urls")),
]
