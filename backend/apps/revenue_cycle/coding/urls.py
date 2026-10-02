from __future__ import annotations

"""Revenue Cycle Coding URL entry point."""

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.revenue_cycle.coding.api.urls"),
    ),
]

__all__ = ("urlpatterns",)
