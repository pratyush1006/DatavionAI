"""
URL configuration for the Master Patient Index API.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.mpi.api.views import (
    MPICreateAPIView,
    MPIDestroyAPIView,
    MPIListAPIView,
    MPIRetrieveAPIView,
    MPIUpdateAPIView,
)

app_name = "patient-mpi"

urlpatterns = [
    path(
        "",
        MPIListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        MPICreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<uuid:pk>/",
        MPIRetrieveAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:pk>/update/",
        MPIUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:pk>/delete/",
        MPIDestroyAPIView.as_view(),
        name="delete",
    ),
]
