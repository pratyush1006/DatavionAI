"""
Medication API URLs.
"""

from django.urls import path

from apps.medications.api.views import (
    MedicationListCreateAPIView,
    MedicationRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        MedicationListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:medication_id>/",
        MedicationRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]

__all__ = [
    "urlpatterns",
]
