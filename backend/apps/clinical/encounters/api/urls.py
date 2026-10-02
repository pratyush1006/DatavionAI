from django.urls import path

from .views import (
    EncounterDetailAPIView,
    EncounterLifecycleAPIView,
    EncounterListCreateAPIView,
)

urlpatterns = [
    path("", EncounterListCreateAPIView.as_view(), name="list-create"),
    path("<uuid:encounter_id>/", EncounterDetailAPIView.as_view(), name="detail"),
    path(
        "<uuid:encounter_id>/<str:action>/",
        EncounterLifecycleAPIView.as_view(),
        name="lifecycle",
    ),
]
