from __future__ import annotations

"""Revenue Cycle Coding API URL routes."""

from django.urls import path

from .views import (
    CodeAssignmentAPIView,
    CodingDetailAPIView,
    CodingListCreateAPIView,
    CodingRestoreAPIView,
    CodingTransitionAPIView,
)

app_name = "revenue_cycle_api"

urlpatterns = [
    path(
        "",
        CodingListCreateAPIView.as_view(),
        name="coding-list-create",
    ),
    path(
        "<uuid:record_id>/",
        CodingDetailAPIView.as_view(),
        name="coding-detail",
    ),
    path(
        "<uuid:record_id>/transition/",
        CodingTransitionAPIView.as_view(),
        name="coding-transition",
    ),
    path(
        "<uuid:record_id>/codes/",
        CodeAssignmentAPIView.as_view(),
        name="coding-code-assignment",
    ),
    path(
        "<uuid:record_id>/restore/",
        CodingRestoreAPIView.as_view(),
        name="coding-restore",
    ),
]

__all__ = ("urlpatterns",)
