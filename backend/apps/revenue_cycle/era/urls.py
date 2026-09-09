"""URL configuration for Revenue Cycle ERA."""

from __future__ import annotations

from django.urls import path

from .api.views import (
    ERADetailAPIView,
    ERAListCreateAPIView,
    ERAPostAPIView,
    ERARestoreAPIView,
    ERAReverseAPIView,
    ERAValidateAPIView,
)

app_name = "revenue_cycle_era"

urlpatterns = (
    path("", ERAListCreateAPIView.as_view(), name="list-create"),
    path("<uuid:era_id>/", ERADetailAPIView.as_view(), name="detail"),
    path("<uuid:era_id>/validate/", ERAValidateAPIView.as_view(), name="validate"),
    path("<uuid:era_id>/post/", ERAPostAPIView.as_view(), name="post"),
    path("<uuid:era_id>/reverse/", ERAReverseAPIView.as_view(), name="reverse"),
    path("<uuid:era_id>/restore/", ERARestoreAPIView.as_view(), name="restore"),
)

__all__ = ("app_name", "urlpatterns")
