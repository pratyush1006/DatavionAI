"""
URL configuration for laboratory test APIs.
"""

from __future__ import annotations

from django.urls import path

from apps.laboratories.api.views.laboratory_test import (
    LaboratoryTestCancelAPIView,
    LaboratoryTestCompleteAPIView,
    LaboratoryTestListCreateAPIView,
    LaboratoryTestRetrieveUpdateDestroyAPIView,
    LaboratoryTestStartAPIView,
)

app_name = "laboratory_test"

urlpatterns = [
    path(
        "",
        LaboratoryTestListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:uuid>/",
        LaboratoryTestRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path(
        "<uuid:uuid>/start/",
        LaboratoryTestStartAPIView.as_view(),
        name="start",
    ),
    path(
        "<uuid:uuid>/complete/",
        LaboratoryTestCompleteAPIView.as_view(),
        name="complete",
    ),
    path(
        "<uuid:uuid>/cancel/",
        LaboratoryTestCancelAPIView.as_view(),
        name="cancel",
    ),
]
