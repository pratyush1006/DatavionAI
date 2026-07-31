"""
URL patterns for the AR Record module.
"""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.ar.api.views import (
    AccountsReceivableListCreateAPIView,
    AccountsReceivableRetrieveUpdateDestroyAPIView,
)

app_name = "ar_records"

urlpatterns = [
    path(
        "",
        AccountsReceivableListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:ar_id>/",
        AccountsReceivableRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
