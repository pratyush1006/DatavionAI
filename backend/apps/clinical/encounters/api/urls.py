"""
Encounter API URLs.
"""

from django.urls import path

from apps.clinical.encounters.api.views import (
    EncounterListCreateAPIView,
    EncounterRetrieveUpdateDestroyAPIView,
)

app_name = "encounters"

urlpatterns = [
    path(
        "",
        EncounterListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:encounter_id>/",
        EncounterRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
]
