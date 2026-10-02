"""Patient Communication API routes."""

from __future__ import annotations

from django.urls import path

from apps.patient_management.communication.api.views import (
    CommunicationLifecycleView,
    CommunicationListCreateView,
    CommunicationRetrieveUpdateDestroyView,
)

urlpatterns = [
    path("", CommunicationListCreateView.as_view(), name="communication-list-create"),
    path(
        "<uuid:communication_id>/",
        CommunicationRetrieveUpdateDestroyView.as_view(),
        name="communication-detail",
    ),
    path(
        "<uuid:communication_id>/lifecycle/",
        CommunicationLifecycleView.as_view(),
        name="communication-lifecycle",
    ),
]

__all__ = ("urlpatterns",)
