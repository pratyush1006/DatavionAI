from __future__ import annotations

from unittest.mock import Mock, patch

from django.test import SimpleTestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from apps.core.workflows import workflow_registry
from apps.telemedicine.api.views.session import TelemedicineSessionDetailAPIView
from apps.telemedicine.constants import (
    MediaPermission,
    ParticipantStatus,
    SessionStatus,
)
from apps.telemedicine.integrations.video_provider import Room, get_video_provider
from apps.telemedicine.services.participant import ALLOWED as PARTICIPANT_TRANSITIONS
from apps.telemedicine.services.session import ALLOWED_TRANSITIONS
from apps.telemedicine.tasks.provisioning import provision_session_room
from apps.telemedicine.workflow_registry import register_telemedicine_workflows


class TelemedicineLifecycleTests(SimpleTestCase):
    def test_session_lifecycle(self):
        self.assertIn(SessionStatus.SCHEDULED, ALLOWED_TRANSITIONS[SessionStatus.DRAFT])
        self.assertIn(
            SessionStatus.CONFIRMED, ALLOWED_TRANSITIONS[SessionStatus.SCHEDULED]
        )
        self.assertIn(SessionStatus.READY, ALLOWED_TRANSITIONS[SessionStatus.CONFIRMED])
        self.assertIn(
            SessionStatus.IN_PROGRESS, ALLOWED_TRANSITIONS[SessionStatus.READY]
        )
        self.assertIn(
            SessionStatus.COMPLETED, ALLOWED_TRANSITIONS[SessionStatus.IN_PROGRESS]
        )

    def test_terminal_states_are_closed(self):
        for state in (
            SessionStatus.COMPLETED,
            SessionStatus.CANCELLED,
            SessionStatus.NO_SHOW,
            SessionStatus.FAILED,
        ):
            self.assertEqual(ALLOWED_TRANSITIONS[state], set())

    def test_participant_lifecycle(self):
        self.assertIn(
            ParticipantStatus.ADMITTED,
            PARTICIPANT_TRANSITIONS[ParticipantStatus.INVITED],
        )
        self.assertIn(
            ParticipantStatus.JOINED,
            PARTICIPANT_TRANSITIONS[ParticipantStatus.ADMITTED],
        )
        self.assertIn(
            ParticipantStatus.LEFT, PARTICIPANT_TRANSITIONS[ParticipantStatus.JOINED]
        )

    def test_media_permissions(self):
        self.assertEqual(
            set(MediaPermission.values),
            {"prompt", "granted", "denied", "not_applicable"},
        )


class TelemedicineWorkflowTests(SimpleTestCase):
    def test_workflows_registered(self):
        register_telemedicine_workflows()
        names = (
            "telemedicine.session.create",
            "telemedicine.session.schedule",
            "telemedicine.session.confirm",
            "telemedicine.session.prepare",
            "telemedicine.session.start",
            "telemedicine.session.complete",
            "telemedicine.session.cancel",
            "telemedicine.session.no_show",
            "telemedicine.session.fail",
            "telemedicine.participant.invite",
            "telemedicine.participant.admit",
            "telemedicine.participant.join",
            "telemedicine.participant.leave",
            "telemedicine.participant.media_state",
            "telemedicine.recording.start",
            "telemedicine.recording.finalize",
        )
        for name in names:
            self.assertTrue(workflow_registry.is_registered(name), name)


class TestVideoProvider:
    def create_room(self, *, session_id, session_type):
        return Room(
            connection_id="room-" + session_id,
            connection_url="https://example.invalid/room",
            provider_name="test",
        )

    def create_participant_token(self, *, connection_id, participant_id, display_name):
        return Mock(token="test-token", expires_at=None)

    def close_room(self, *, connection_id):
        return None

    def start_recording(self, *, connection_id):
        return "recording-test"

    def stop_recording(self, *, connection_id, recording_id):
        return None


class TelemedicineProviderTests(SimpleTestCase):
    @patch("apps.telemedicine.integrations.video_provider.settings")
    def test_provider_required(self, settings_mock):
        settings_mock.TELEMEDICINE_VIDEO_PROVIDER = ""
        with self.assertRaisesRegex(RuntimeError, "TELEMEDICINE_VIDEO_PROVIDER"):
            get_video_provider()

    @patch("apps.telemedicine.integrations.video_provider.settings")
    def test_provider_loads(self, settings_mock):
        settings_mock.TELEMEDICINE_VIDEO_PROVIDER = (
            "apps.telemedicine.tests.test_production.TestVideoProvider"
        )
        self.assertIsInstance(get_video_provider(), TestVideoProvider)


class TelemedicineProvisioningTests(SimpleTestCase):
    @patch("apps.telemedicine.tasks.provisioning.SessionService.prepare")
    def test_provisioning_delegates(self, prepare_mock):
        s = Mock(
            session_id="session-id",
            organization_id="organization-id",
            status=SessionStatus.READY,
            connection_id="connection-id",
            connection_url="https://example.invalid",
            provider_name="test",
        )
        prepare_mock.return_value = s
        result = provision_session_room.run(
            session_id="session-id", organization_id="organization-id"
        )
        prepare_mock.assert_called_once_with(
            session_id="session-id", organization_id="organization-id"
        )
        self.assertEqual(result["status"], SessionStatus.READY)


class TelemedicineApiSecurityTests(SimpleTestCase):
    def test_session_detail_requires_view_permission(self):
        request = APIRequestFactory().get("/api/telemedicine/sessions/test/")
        user = Mock(is_authenticated=True, id="actor")
        force_authenticate(request, user=user)
        request.tenant = Mock(id="tenant")
        request.organization = Mock(id="organization", tenant_id="tenant")
        with (
            patch(
                "apps.telemedicine.api.views.session.require_tenant_organization",
                return_value=(request.tenant, request.organization),
            ),
            patch(
                "apps.telemedicine.api.views.session.resolve_permissions",
                return_value=set(),
            ),
        ):
            response = TelemedicineSessionDetailAPIView.as_view()(
                request, session_id="00000000-0000-0000-0000-000000000000"
            )
        self.assertEqual(response.status_code, 403)

    def test_session_detail_requires_authentication(self):
        request = APIRequestFactory().get("/api/telemedicine/sessions/test/")
        response = TelemedicineSessionDetailAPIView.as_view()(
            request, session_id="00000000-0000-0000-0000-000000000000"
        )
        self.assertEqual(response.status_code, 401)
