"""URL routes for Patient Documents."""

from __future__ import annotations

from django.urls import path

from apps.patient_management.patient_documents.api.views import (
    PatientDocumentAccessAuditAPIView,
    PatientDocumentActivationAPIView,
    PatientDocumentArchiveAPIView,
    PatientDocumentDeleteAPIView,
    PatientDocumentDetailAPIView,
    PatientDocumentListCreateAPIView,
    PatientDocumentRestoreAPIView,
    PatientDocumentUpdateAPIView,
    PatientDocumentVersionListCreateAPIView,
)

app_name = "patient_documents"

urlpatterns = [
    path(
        "<uuid:document_id>/versions/",
        PatientDocumentVersionListCreateAPIView.as_view(),
        name="versions",
    ),
    path(
        "<uuid:document_id>/access-audit/",
        PatientDocumentAccessAuditAPIView.as_view(),
        name="access-audit",
    ),
    path(
        "",
        PatientDocumentListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:document_id>/",
        PatientDocumentDetailAPIView.as_view(),
        name="detail",
    ),
    path(
        "<uuid:document_id>/update/",
        PatientDocumentUpdateAPIView.as_view(),
        name="update",
    ),
    path(
        "<uuid:document_id>/delete/",
        PatientDocumentDeleteAPIView.as_view(),
        name="delete",
    ),
    path(
        "<uuid:document_id>/activate/",
        PatientDocumentActivationAPIView.as_view(),
        name="activate",
    ),
    path(
        "<uuid:document_id>/archive/",
        PatientDocumentArchiveAPIView.as_view(),
        name="archive",
    ),
    path(
        "<uuid:document_id>/restore/",
        PatientDocumentRestoreAPIView.as_view(),
        name="restore",
    ),
]


__all__ = (
    "app_name",
    "urlpatterns",
)
