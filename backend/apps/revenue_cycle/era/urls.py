"""
URL patterns for the Remittance Advice module.
"""

from __future__ import annotations

from apps.revenue_cycle.era.api.views import (
    RemittanceAdviceListCreateAPIView,
    RemittanceAdviceRetrieveUpdateDestroyAPIView,
)
from django.urls import path

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
