"""
Document API URLs.
"""

from __future__ import annotations

from django.urls import path

from apps.documents.api.views import (
    DocumentListCreateAPIView,
    DocumentRetrieveUpdateDestroyAPIView,
)
from apps.documents.api.views.media import (
    DocumentDownloadAPIView,
    DocumentUploadAPIView,
)

app_name = "documents-api"


urlpatterns = [
    path("upload/", DocumentUploadAPIView.as_view(), name="document-upload"),
    path(
        "",
        DocumentListCreateAPIView.as_view(),
        name="document-list-create",
    ),
    path(
        "<uuid:uuid>/",
        DocumentRetrieveUpdateDestroyAPIView.as_view(),
        name="document-detail",
    ),
    path(
        "<uuid:uuid>/download/",
        DocumentDownloadAPIView.as_view(),
        name="document-download",
    ),
]


__all__ = ("urlpatterns",)
