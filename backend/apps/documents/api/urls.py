"""
Document API URLs.
"""

from __future__ import annotations

from django.urls import path

from apps.documents.api.views import (
    DocumentListCreateAPIView,
    DocumentRetrieveUpdateDestroyAPIView,
)

app_name = "documents-api"


urlpatterns = [
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
]


__all__ = ("urlpatterns",)
