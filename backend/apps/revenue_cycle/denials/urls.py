"""URLs for Revenue Cycle Denials."""

from __future__ import annotations

from django.urls import path

from .api.views import (
    DenialDetailAPIView,
    DenialListCreateAPIView,
    DenialTransitionAPIView,
)

urlpatterns = [
    path("", DenialListCreateAPIView.as_view(), name="denial-list-create"),
    path("<uuid:denial_id>/", DenialDetailAPIView.as_view(), name="denial-detail"),
    path(
        "<uuid:denial_id>/transition/",
        DenialTransitionAPIView.as_view(),
        name="denial-transition",
    ),
]
__all__ = ("urlpatterns",)
