"""
URL configuration for Patient Documents.
"""

from __future__ import annotations

from django.urls import path

from apps.patient_management.patient_documents.api.views import (
    PatientDocumentCreateAPIView,
    PatientDocumentDeleteAPIView,
    PatientDocumentDetailAPIView,
    PatientDocumentListAPIView,
    PatientDocumentUpdateAPIView,
)

app_name = "patient-document-api"

urlpatterns = [
    path(
        "",
        PatientDocumentListAPIView.as_view(),
        name="list",
    ),
    path(
        "create/",
        PatientDocumentCreateAPIView.as_view(),
        name="create",
    ),
    path(
        "<uuid:id>/",
        PatientDocumentDetailAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:id>/update/",
        PatientDocumentUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:id>/delete/",
        PatientDocumentDeleteAPIView.as_view(),
        name="delete",
    ),
]
