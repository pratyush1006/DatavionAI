"""
URL patterns for the Remittance Advice module.
"""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.era.api.views import (
    RemittanceAdviceListCreateAPIView,
    RemittanceAdviceRetrieveUpdateDestroyAPIView,
)

app_name = "remittances"

urlpatterns = [
    path(
        "",
        RemittanceAdviceListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:remittance_id>/",
        RemittanceAdviceRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
