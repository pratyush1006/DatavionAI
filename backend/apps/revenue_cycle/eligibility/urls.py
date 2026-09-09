"""Revenue Cycle Eligibility URL routes."""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.eligibility.api.views import (
    EligibilityDetailAPIView,
    EligibilityLifecycleAPIView,
    EligibilityListCreateAPIView,
    EligibilityRestoreAPIView,
)

app_name = "revenue_cycle_eligibility"
urlpatterns = [
    path("", EligibilityListCreateAPIView.as_view(), name="list-create"),
    path("<uuid:eligibility_id>/", EligibilityDetailAPIView.as_view(), name="detail"),
    path(
        "<uuid:eligibility_id>/lifecycle/",
        EligibilityLifecycleAPIView.as_view(),
        name="lifecycle",
    ),
    path(
        "<uuid:eligibility_id>/restore/",
        EligibilityRestoreAPIView.as_view(),
        name="restore",
    ),
]
__all__ = ("app_name", "urlpatterns")
