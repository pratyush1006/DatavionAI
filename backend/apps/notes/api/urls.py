from django.urls import path

from .views import (
    NoteActionAPIView,
    NoteAmendmentAPIView,
    NoteDetailAPIView,
    NoteListCreateAPIView,
    NoteTemplateListCreateAPIView,
)

urlpatterns = [
    path("", NoteListCreateAPIView.as_view(), name="note-list-create"),
    path("<uuid:note_id>/", NoteDetailAPIView.as_view(), name="note-detail"),
    path(
        "<uuid:note_id>/<str:action>/", NoteActionAPIView.as_view(), name="note-action"
    ),
    path("<uuid:note_id>/amend/", NoteAmendmentAPIView.as_view(), name="note-amend"),
    path("templates/", NoteTemplateListCreateAPIView.as_view(), name="note-templates"),
]
