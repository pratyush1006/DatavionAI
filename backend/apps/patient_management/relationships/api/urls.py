"""
URL configuration for the Patient Relationships API.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.relationships.api.views import (
    RelationshipCreateAPIView,
    RelationshipDestroyAPIView,
    RelationshipListAPIView,
    RelationshipRetrieveAPIView,
    RelationshipUpdateAPIView,
)

app_name = "patient-relationships"

urlpatterns = [
    path(
        "",
        RelationshipListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        RelationshipCreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<uuid:pk>/",
        RelationshipRetrieveAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:pk>/update/",
        RelationshipUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:pk>/delete/",
        RelationshipDestroyAPIView.as_view(),
        name="delete",
    ),
]
