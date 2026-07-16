"""
URL configuration for laboratory order APIs.
"""

from __future__ import annotations

from django.urls import path

from apps.clinical.laboratories.api.views.laboratory_order import (
    LaboratoryOrderListCreateAPIView,
    LaboratoryOrderRetrieveUpdateDestroyAPIView,
)

app_name = "laboratory_order"

urlpatterns = [
    path(
        "",
        LaboratoryOrderListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:uuid>/",
        LaboratoryOrderRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
]
