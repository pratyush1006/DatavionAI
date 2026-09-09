"""Revenue Cycle claim scrubbing URL integration."""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [path("", include("apps.revenue_cycle.claim_scrubbing.api.urls"))]

__all__ = ("urlpatterns",)
