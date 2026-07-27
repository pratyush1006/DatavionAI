"""
Tests for telemedicine models.
"""

from __future__ import annotations

from datetime import datetime

from django.db import IntegrityError
from django.test import TestCase

from apps.clinical.patients.constants import PatientGender
from apps.clinical.providers.constants import ProviderType
from apps.telemedicine.constants import (
    SessionStatus,
    SessionType,
)
from apps.telemedicine.models import (
    Participant,
    Recording,
    TelemedicineSession,
)
from apps.telemedicine.tests.factories import (
    OrganizationFactory,
    ParticipantFactory,
    PatientFactory,
    ProviderFactory,
    RecordingFactory,
    TelemedicineSessionFactory,
)


class TelemedicineSessionModelTestCase(TestCase):
    """
    Test cases for the TelemedicineSession model.
    """

    def setUp(self) -> None:
        self.organization = OrganizationFactory(
            name="Telemedicine Test Organization",
            code="TEL001",
        )

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

        session = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
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

    def test_session_id_generated_on_save(self) -> None:
        """
        Session ID should be generated if not provided.
        """

        session = TelemedicineSession(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            scheduled_start=datetime.now(),
            scheduled_end=datetime.now(),
            status=SessionStatus.SCHEDULED,
            session_type=SessionType.VIDEO,
            connection_url="https://example.com/room/test",
        )

        session.save()

        self.assertIsNotNone(
            session.session_id,
        )

        self.assertNotEqual(
            session.session_id,
            "",
        )

    def test_session_id_unique(self) -> None:
        """
        Session ID should be unique.
        """

        session1 = TelemedicineSessionFactory(
            organization=self.organization,
            session_id="unique-session-1",
        )

        session2 = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            session_id="unique-session-2",
        )

        self.assertNotEqual(
            session1.session_id,
            session2.session_id,
        )

    def test_session_default_status(self) -> None:
        """
        Default session status should be SCHEDULED.
        """

        session = TelemedicineSessionFactory(
            organization=self.organization,
        )

        self.assertEqual(
            session.status,
            SessionStatus.SCHEDULED,
        )

    def test_session_default_type(self) -> None:
        """
        Default session type should be VIDEO.
        """

        session = TelemedicineSessionFactory(
            organization=self.organization,
        )

        self.assertEqual(
            session.session_type,
            SessionType.VIDEO,
        )

    def test_session_str_representation(self) -> None:
        """
        Session string representation should be meaningful.
        """

        session = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
        )

        str_repr = str(session)

        self.assertIn(
            session.session_id,
            str_repr,
        )

        self.assertIn(
            SessionStatus.SCHEDULED,
            str_repr,
        )


class ParticipantModelTestCase(TestCase):
    """
    Test cases for the Participant model.
    """

    def setUp(self) -> None:
        self.organization = OrganizationFactory(
            name="Telemedicine Test Organization 2",
            code="TEL002",
        )

        self.patient = PatientFactory(
            organization=self.organization,
            mrn="MRN000002",
            first_name="Jane",
            last_name="Smith",
            date_of_birth=datetime(1990, 5, 15),
            gender=PatientGender.FEMALE,
        )

        self.provider = ProviderFactory(
            organization=self.organization,
            provider_number="PRV000002",
            license_number="LIC000002",
            provider_type=ProviderType.PHYSICIAN,
        )

        self.session = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
        )

    def test_create_participant(self) -> None:
        """
        Participant should be created successfully.
        """

        participant = ParticipantFactory(
            session=self.session,
        )

        self.assertIsInstance(
            participant,
            Participant,
        )

        self.assertEqual(
            participant.session,
            self.session,
        )

    def test_participant_unique_per_session(self) -> None:
        """
        Same user should not be added to the same session twice.
        """

        from apps.platform.accounts.models import User

        user = User.objects.create_user(
            email="participant@test.com",
            password="TestPassword@123",
            organization=self.organization,
        )

        ParticipantFactory(
            session=self.session,
            user=user,
            participant_type="patient",
        )

        with self.assertRaises(
            IntegrityError,
        ):
            ParticipantFactory(
                session=self.session,
                user=user,
                participant_type="patient",
            )

    def test_participant_str_representation(self) -> None:
        """
        Participant string representation should be meaningful.
        """

        from apps.platform.accounts.models import User

        user = User.objects.create_user(
            email="participant2@test.com",
            password="TestPassword@123",
            organization=self.organization,
            first_name="Alice",
            last_name="Patient",
        )

        participant = ParticipantFactory(
            session=self.session,
            user=user,
            participant_type="patient",
        )

        str_repr = str(participant)

        self.assertIn(
            user.full_name,
            str_repr,
        )

        self.assertIn(
            "patient",
            str_repr,
        )

        self.assertIn(
            self.session.session_id,
            str_repr,
        )


class RecordingModelTestCase(TestCase):
    """
    Test cases for the Recording model.
    """

    def setUp(self) -> None:
        self.organization = OrganizationFactory(
            name="Telemedicine Test Organization 3",
            code="TEL003",
        )

        self.patient = PatientFactory(
            organization=self.organization,
            mrn="MRN000003",
            first_name="Bob",
            last_name="Johnson",
            date_of_birth=datetime(1985, 8, 10),
            gender=PatientGender.MALE,
        )

        self.provider = ProviderFactory(
            organization=self.organization,
            provider_number="PRV000003",
            license_number="LIC000003",
            provider_type=ProviderType.PHYSICIAN,
        )

        self.session = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
        )

    def test_create_recording(self) -> None:
        """
        Recording should be created successfully.
        """

        recording = RecordingFactory(
            session=self.session,
        )

        self.assertIsInstance(
            recording,
            Recording,
        )

        self.assertEqual(
            recording.session,
            self.session,
        )

    def test_recording_default_not_processed(self) -> None:
        """
        Recording should not be processed by default.
        """

        recording = RecordingFactory(
            session=self.session,
        )

        self.assertFalse(
            recording.is_processed,
        )

    def test_recording_str_representation(self) -> None:
        """
        Recording string representation should be meaningful.
        """

        recording = RecordingFactory(
            session=self.session,
            duration_seconds=1800,
        )

        str_repr = str(recording)

        self.assertIn(
            self.session.session_id,
            str_repr,
        )

        self.assertIn(
            "1800s",
            str_repr,
        )


__all__ = [
    "ParticipantModelTestCase",
    "RecordingModelTestCase",
    "TelemedicineSessionModelTestCase",
]
