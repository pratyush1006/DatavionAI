"""
Tests for telemedicine selectors.
"""

from __future__ import annotations

from datetime import (
    datetime,
    timedelta,
)

from django.test import TestCase
from django.utils import timezone

from apps.clinical.patients.constants import PatientGender
from apps.clinical.providers.constants import ProviderType
from apps.telemedicine.constants import (
    SessionStatus,
)
from apps.telemedicine.selectors import SessionSelector
from apps.telemedicine.tests.factories import (
    OrganizationFactory,
    PatientFactory,
    ProviderFactory,
    TelemedicineSessionFactory,
)


class SessionSelectorTestCase(TestCase):
    """
    Test cases for SessionSelector.
    """

    def setUp(self) -> None:
        self.organization = OrganizationFactory(
            name="Test Organization",
            code="TST004",
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

        self.session = TelemedicineSessionFactory(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
        )

    def test_list_sessions(self) -> None:
        """
        All sessions should be returned.
        """

        sessions = SessionSelector.list()

        self.assertIn(
            self.session,
            sessions,
        )

    def test_get_session_by_id(self) -> None:
        """
        Session should be retrieved by identifier.
        """

        retrieved = SessionSelector.get(
            session_id=self.session.id,
        )

        self.assertEqual(
            retrieved.id,
            self.session.id,
        )

    def test_list_by_patient(self) -> None:
        """
        Sessions for a patient should be returned.
        """

        sessions = SessionSelector.list_by_patient(
            patient_id=self.patient.id,
        )

        self.assertIn(
            self.session,
            sessions,
        )

    def test_list_by_provider(self) -> None:
        """
        Sessions for a provider should be returned.
        """

        sessions = SessionSelector.list_by_provider(
            provider_id=self.provider.id,
        )

        self.assertIn(
            self.session,
            sessions,
        )

    def test_list_by_organization(self) -> None:
        """
        Sessions for an organization should be returned.
        """

        sessions = SessionSelector.list_by_organization(
            organization=self.organization,
        )

        self.assertIn(
            self.session,
            sessions,
        )

    def test_list_by_status(self) -> None:
        """
        Sessions with a specific status should be returned.
        """

        sessions = SessionSelector.list_by_status(
            status=SessionStatus.SCHEDULED,
            organization=self.organization,
        )

        self.assertIn(
            self.session,
            sessions,
        )

    def test_list_by_date_range(self) -> None:
        """
        Sessions within a date range should be returned.
        """

        start_date = timezone.now() - timedelta(days=7)
        end_date = timezone.now() + timedelta(days=7)

        sessions = SessionSelector.list_by_date_range(
            start_date=start_date,
            end_date=end_date,
            organization=self.organization,
        )

        self.assertIn(
            self.session,
            sessions,
        )

    def test_search_sessions(self) -> None:
        """
        Sessions matching a search query should be returned.
        """

        sessions = SessionSelector.search(
            organization=self.organization,
            query="John",
        )

        self.assertIn(
            self.session,
            sessions,
        )

    def test_search_sessions_by_provider_name(self) -> None:
        """
        Sessions matching a provider name should be returned.
        """

        sessions = SessionSelector.search(
            organization=self.organization,
            query=self.provider.employee.user.first_name,
        )

        self.assertIn(
            self.session,
            sessions,
        )

    def test_count_sessions(self) -> None:
        """
        Session count should match.
        """

        count = SessionSelector.count(
            organization=self.organization,
        )

        self.assertGreaterEqual(
            count,
            1,
        )

    def test_count_sessions_by_status(self) -> None:
        """
        Session count by status should match.
        """

        count = SessionSelector.count(
            organization=self.organization,
            status=SessionStatus.SCHEDULED,
        )

        self.assertGreaterEqual(
            count,
            1,
        )


__all__ = [
    "SessionSelectorTestCase",
]
