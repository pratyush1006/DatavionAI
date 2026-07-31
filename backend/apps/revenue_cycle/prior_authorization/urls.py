"""
URL patterns for the Prior Authorization module.
"""

from __future__ import annotations

from django.urls import path

from apps.revenue_cycle.prior_authorization.api.views import (
    PriorAuthorizationRequestListCreateAPIView,
    PriorAuthorizationRequestRetrieveUpdateDestroyAPIView,
)

app_name = "prior_authorizations"

urlpatterns = [
    path(
        "",
        PriorAuthorizationRequestListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:authorization_id>/",
        PriorAuthorizationRequestRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "app_name",
    "urlpatterns",
]
