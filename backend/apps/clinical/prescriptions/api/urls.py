"""Workflow-driven API routes for Prescription."""

from django.urls import path

from .views import (
    PrescriptionDetailAPIView,
    PrescriptionLifecycleAPIView,
    PrescriptionListCreateAPIView,
)

urlpatterns = [
    path("", PrescriptionListCreateAPIView.as_view(), name="list-create"),
    path("<uuid:prescription_id>/", PrescriptionDetailAPIView.as_view(), name="detail"),
    path(
        "<uuid:prescription_id>/lifecycle/",
        PrescriptionLifecycleAPIView.as_view(),
        name="lifecycle",
    ),
]
