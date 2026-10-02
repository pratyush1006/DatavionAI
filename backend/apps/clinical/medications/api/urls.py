from django.urls import path

from apps.clinical.medications.api.views import (
    MedicationListCreateAPIView,
    MedicationRetrieveUpdateDestroyAPIView,
)

app_name = "medications"

urlpatterns = [
    path("", MedicationListCreateAPIView.as_view(), name="list-create"),
    path(
        "<uuid:medication_id>/",
        MedicationRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]
