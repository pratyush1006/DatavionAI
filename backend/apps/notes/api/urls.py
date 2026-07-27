"""
Note API URL patterns.
"""

from __future__ import annotations

from django.urls import path

from apps.notes.api.views import (
    NoteBulkCreateAPIView,
    NoteListCreateAPIView,
    NoteRetrieveUpdateDestroyAPIView,
    NoteTemplateListCreateAPIView,
    NoteTemplateRetrieveUpdateDestroyAPIView,
)

app_name = "notes"

urlpatterns = [
    path(
        "templates/",
        NoteTemplateListCreateAPIView.as_view(),
        name="template-list-create",
    ),
    path(
        "templates/<uuid:template_id>/",
        NoteTemplateRetrieveUpdateDestroyAPIView.as_view(),
        name="template-detail",
    ),
    path(
        "",
        NoteListCreateAPIView.as_view(),
        name="list-create",
    ),
    path(
        "<uuid:note_id>/",
        NoteRetrieveUpdateDestroyAPIView.as_view(),
        name="detail",
    ),
    path(
        "patient/<uuid:patient_id>/",
        NoteListCreateAPIView.as_view(),
        name="list-by-patient",
    ),
    path(
        "encounter/<uuid:encounter_id>/",
        NoteListCreateAPIView.as_view(),
        name="list-by-encounter",
    ),
    path(
        "bulk/",
        NoteBulkCreateAPIView.as_view(),
        name="bulk-create",
    ),
]
