"""
Revenue Cycle Appeals API routes.
"""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.appeals.api.views import (
    AppealDeleteAPIView,
    AppealListCreateAPIView,
    AppealRestoreAPIView,
    AppealRetrieveUpdateAPIView,
    AppealTransitionAPIView,
)

app_name = "revenue_cycle_appeals_api"

urlpatterns = [
    path(
        "",
        AppealListCreateAPIView.as_view(),
        name="appeal-list-create",
    ),
    path(
        "<uuid:appeal_id>/",
        AppealRetrieveUpdateAPIView.as_view(),
        name="appeal-detail",
    ),
    path(
        "<uuid:appeal_id>/transition/",
        AppealTransitionAPIView.as_view(),
        name="appeal-transition",
    ),
    path(
        "<uuid:appeal_id>/delete/",
        AppealDeleteAPIView.as_view(),
        name="appeal-delete",
    ),
    path(
        "<uuid:appeal_id>/restore/",
        AppealRestoreAPIView.as_view(),
        name="appeal-restore",
    ),
]


__all__ = ("urlpatterns",)
