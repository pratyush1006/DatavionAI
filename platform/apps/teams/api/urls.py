from django.urls import path

from apps.teams.api.views import (
    TeamListCreateAPIView,
    TeamRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path(
        "",
        TeamListCreateAPIView.as_view(),
        name="team-list-create",
    ),
    path(
        "<int:team_id>/",
        TeamRetrieveUpdateDestroyAPIView.as_view(),
        name="team-detail",
    ),
]
