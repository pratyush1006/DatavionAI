from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.notes.api.views import NoteActionAPIView, NoteListCreateAPIView


class ClinicalNoteAPIPermissionTests(SimpleTestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.organization = SimpleNamespace(pk=uuid4(), id=uuid4())
        self.user = SimpleNamespace(pk=uuid4(), is_authenticated=True, is_active=True)

    def _request(self, request):
        request.organization = self.organization
        force_authenticate(request, user=self.user)
        return request

    @patch(
        "apps.platform.rbac.permissions.base.user_has_permission", return_value=False
    )
    def test_note_list_requires_notes_view_grant(self, has_permission):
        request = self._request(self.factory.get("/api/notes/"))

        response = NoteListCreateAPIView.as_view()(request)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(has_permission.call_args.kwargs["permission"], "notes.view")

    @patch(
        "apps.platform.rbac.permissions.base.user_has_permission", return_value=False
    )
    def test_note_sign_action_requires_notes_sign_grant(self, has_permission):
        note_id = uuid4()
        request = self._request(self.factory.post(f"/api/notes/{note_id}/sign/"))

        response = NoteActionAPIView.as_view()(request, note_id=note_id, action="sign")

        self.assertEqual(response.status_code, 403)
        self.assertEqual(has_permission.call_args.kwargs["permission"], "notes.sign")
