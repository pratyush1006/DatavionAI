"""Revenue Cycle Prior Authorization URL routes."""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.prior_authorization.api.views import (
    PriorAuthorizationDetailAPIView,
    PriorAuthorizationLifecycleAPIView,
    PriorAuthorizationListCreateAPIView,
    PriorAuthorizationRestoreAPIView,
)

app_name = "revenue_cycle_prior_authorization"

urlpatterns = (
    path("", PriorAuthorizationListCreateAPIView.as_view(), name="list-create"),
    path(
        "<uuid:verification_id>/",
        PriorAuthorizationDetailAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:verification_id>/lifecycle/",
        PriorAuthorizationLifecycleAPIView.as_view(),
        name="lifecycle",
    ),
    path(
        "<uuid:verification_id>/restore/",
        PriorAuthorizationRestoreAPIView.as_view(),
        name="restore",
    ),
)

__all__ = ("app_name", "urlpatterns")
