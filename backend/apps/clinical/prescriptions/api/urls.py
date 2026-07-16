"""
Prescription API URLs.
"""

from django.urls import path

from apps.clinical.prescriptions.api.views import (
    PrescriptionListCreateAPIView,
    PrescriptionRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        PrescriptionListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:prescription_id>/",
        PrescriptionRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "urlpatterns",
]
