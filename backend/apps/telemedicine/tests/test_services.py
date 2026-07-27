"""
Tests for telemedicine services.
"""

from __future__ import annotations

from datetime import (
    datetime,
    timedelta,
)

from django.utils import timezone

from apps.clinical.patients.constants import PatientGender
from apps.clinical.providers.constants import ProviderType
from apps.common.tests.base import BaseTestCase
from apps.telemedicine.constants import (
    SessionStatus,
    SessionType,
)
from apps.telemedicine.models import TelemedicineSession
from apps.telemedicine.services import SessionService
from apps.telemedicine.tests.factories import (
    PatientFactory,
    ProviderFactory,
    TelemedicineSessionFactory,
)


class SessionServiceTestCase(BaseTestCase):
    """
    Test cases for SessionService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = PatientFactory(
            organization=self.organization,
            mrn="MRN000001",
            first_name="John",
            last_name="Doe",
            date_of_birth=datetime(1995, 1, 1),
            gender=PatientGender.MALE,
        )

        self.provider = ProviderFactory(
            organization=self.organization,
            provider_number="PRV000001",
            license_number="LIC000001",
            provider_type=ProviderType.PHYSICIAN,
        )

    def test_create_session(self) -> None:
        """
        Session should be created successfully.
        """

        session = SessionService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "scheduled_start": timezone.now(),
                "scheduled_end": timezone.now() + timedelta(hours=1),
                "status": SessionStatus.SCHEDULED,
                "session_type": SessionType.VIDEO,
                "connection_url": "https://example.com/room/test",
            },
        )

        self.assertIsInstance(
            session,
            TelemedicineSession,
        )

        self.assertEqual(
            session.organization,
            self.organization,
        )

        self.assertEqual(
            session.patient,
            self.patient,
        )

        self.assertEqual(
            session.provider,
            self.provider,
        )

    def test_create_session_persists_to_database(self) -> None:
        """
        Created session should be persisted.
        """

        initial_count = TelemedicineSession.objects.count()

        SessionService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "scheduled_start": timezone.now(),
                "scheduled_end": timezone.now() + timedelta(hours=1),
                "status": SessionStatus.SCHEDULED,
                "session_type": SessionType.VIDEO,
                "connection_url": "https://example.com/room/test",
            },
        )

        self.assertEqual(
            TelemedicineSession.objects.count(),
            initial_count + 1,
        )

    def test_update_session(self) -> None:
        """
        Session should be updated successfully.
        """

        session = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
        )

        updated_session = SessionService.update(
            instance=session,
            validated_data={
                "status": SessionStatus.CANCELLED,
                "notes": "Patient requested cancellation.",
            },
        )

        updated_session.refresh_from_db()

        self.assertEqual(
            updated_session.status,
            SessionStatus.CANCELLED,
        )

        self.assertEqual(
            updated_session.notes,
            "Patient requested cancellation.",
        )

    def test_start_session(self) -> None:
        """
        Session should be started successfully.
        """

        session = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            status=SessionStatus.SCHEDULED,
        )

        started_session = SessionService.start(
            instance=session,
        )

        started_session.refresh_from_db()

        self.assertEqual(
            started_session.status,
            SessionStatus.IN_PROGRESS,
        )

        self.assertIsNotNone(
            started_session.actual_start,
        )

    def test_end_session(self) -> None:
        """
        Session should be ended successfully.
        """

        session = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            status=SessionStatus.IN_PROGRESS,
        )

        ended_session = SessionService.end(
            instance=session,
        )

        ended_session.refresh_from_db()

        self.assertEqual(
            ended_session.status,
            SessionStatus.COMPLETED,
        )

        self.assertIsNotNone(
            ended_session.actual_end,
        )

    def test_cancel_session(self) -> None:
        """
        Session should be cancelled successfully.
        """

        session = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            status=SessionStatus.SCHEDULED,
        )

        cancelled_session = SessionService.cancel(
            instance=session,
        )

        cancelled_session.refresh_from_db()

        self.assertEqual(
            cancelled_session.status,
            SessionStatus.CANCELLED,
        )

    def test_bulk_create_sessions(self) -> None:
        """
        Multiple sessions should be created successfully.
        """

        sessions = SessionService.bulk_create(
            validated_data_list=[
                {
                    "organization": self.organization,
                    "patient": self.patient,
                    "provider": self.provider,
                    "scheduled_start": timezone.now(),
                    "scheduled_end": timezone.now() + timedelta(hours=1),
                    "status": SessionStatus.SCHEDULED,
                    "session_type": SessionType.VIDEO,
                    "connection_url": "https://example.com/room/1",
                },
                {
                    "organization": self.organization,
                    "patient": self.patient,
                    "provider": self.provider,
                    "scheduled_start": timezone.now() + timedelta(hours=2),
                    "scheduled_end": timezone.now() + timedelta(hours=3),
                    "status": SessionStatus.SCHEDULED,
                    "session_type": SessionType.AUDIO,
                    "connection_url": "https://example.com/room/2",
                },
            ],
        )

        self.assertEqual(
            len(sessions),
            2,
        )

        self.assertIsInstance(
            sessions[0],
            TelemedicineSession,
        )

        self.assertIsInstance(
            sessions[1],
            TelemedicineSession,
        )

    def test_start_updates_actual_start(self) -> None:
        """
        Starting a session should set actual_start to approximately now.
        """

        session = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            status=SessionStatus.SCHEDULED,
        )

        before_start = timezone.now()

        started_session = SessionService.start(
            instance=session,
        )

        after_start = timezone.now()

        self.assertTrue(
            before_start <= started_session.actual_start <= after_start,
        )


__all__ = [
    "SessionServiceTestCase",
]
