"""HTTP routes for Revenue Cycle Charge Capture."""

from __future__ import annotations

from django.urls import path

from .views import (
    ChargeDetailView,
    ChargeListCreateView,
    ChargeTransitionView,
    ChargeVoidView,
)

__all__ = ("urlpatterns",)

urlpatterns = [
    path("charges/", ChargeListCreateView.as_view(), name="charge-list-create"),
    path("charges/<uuid:charge_id>/", ChargeDetailView.as_view(), name="charge-detail"),
    path(
        "charges/<uuid:charge_id>/transition/",
        ChargeTransitionView.as_view(),
        name="charge-transition",
    ),
    path(
        "charges/<uuid:charge_id>/void/",
        ChargeVoidView.as_view(),
        name="charge-void",
    ),
]
