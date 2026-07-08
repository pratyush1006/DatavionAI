"""
URL configuration for laboratory result APIs.
"""

from __future__ import annotations

from django.urls import path

from apps.laboratories.api.views.laboratory_result import (
    LaboratoryResultAmendAPIView,
    LaboratoryResultInvalidateAPIView,
    LaboratoryResultListCreateAPIView,
    LaboratoryResultRecordAPIView,
    LaboratoryResultRetrieveUpdateDestroyAPIView,
    LaboratoryResultVerifyAPIView,
)

app_name = "laboratory_result"

urlpatterns = [
    path(
        "",
        LaboratoryResultListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:uuid>/",
        LaboratoryResultRetrieveUpdateDestroyAPIView.as_view(),
        name="retrieve-update-destroy",
    ),
    path(
        "<uuid:uuid>/record/",
        LaboratoryResultRecordAPIView.as_view(),
        name="record",
    ),
    path(
        "<uuid:uuid>/verify/",
        LaboratoryResultVerifyAPIView.as_view(),
        name="verify",
    ),
    path(
        "<uuid:uuid>/amend/",
        LaboratoryResultAmendAPIView.as_view(),
        name="amend",
    ),
    path(
        "<uuid:uuid>/invalidate/",
        LaboratoryResultInvalidateAPIView.as_view(),
        name="invalidate",
    ),
]
