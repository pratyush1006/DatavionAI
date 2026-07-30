"""
URL patterns for the Eligibility Check module.
"""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.eligibility.api.views import (
    EligibilityCheckListCreateAPIView,
    EligibilityCheckRetrieveUpdateDestroyAPIView,
)

app_name = "eligibility_checks"

urlpatterns = [
    path(
        "",
        EligibilityCheckListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:eligibility_id>/",
        EligibilityCheckRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
