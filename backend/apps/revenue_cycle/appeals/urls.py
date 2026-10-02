"""
Revenue Cycle Appeals URL configuration.
"""

from __future__ import annotations

from django.urls import include, path

urlpatterns = [
    path(
        "",
        include("apps.revenue_cycle.appeals.api.urls"),
    ),
]


__all__ = ("urlpatterns",)
