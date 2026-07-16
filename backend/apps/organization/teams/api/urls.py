"""
API routes for Teams.
"""

from apps.organization.teams.api.views import (
    TeamListCreateAPIView,
    TeamRetrieveUpdateDestroyAPIView,
)
from django.urls import path

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
