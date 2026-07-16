"""
Tests for the Encounter model.
"""

from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from apps.clinical.encounters.constants import EncounterStatus
from apps.clinical.encounters.models import Encounter
from apps.common.tests.base import BaseTestCase


class EncounterModelTestCase(BaseTestCase):
    """
    Test cases for the Encounter model.
    """

    def setUp(
        self,
    ) -> None:
        """
        Set up test data.
        """

        super().setUp()

        self.employee = self.create_employee(
            organization=self.organization,
        )

        self.provider = self.create_provider(
            organization=self.organization,
            employee=self.employee,
        )

        self.patient = self.create_patient(
            organization=self.organization,
        )

        self.appointment = self.create_appointment(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
        )

        self.encounter = Encounter.objects.create(
            organization=self.organization,
            appointment=self.appointment,
            patient=self.patient,
            provider=self.provider,
            encounter_number="ENC000001",
            status=EncounterStatus.SCHEDULED,
            chief_complaint="Fever",
            started_at=timezone.now(),
            ended_at=timezone.now()
            + timedelta(
                minutes=30,
            ),
            duration_minutes=30,
        )

    def test_str(
        self,
    ) -> None:
        """
        String representation should be correct.
        """

        self.assertEqual(
            str(self.encounter),
            (
                f"{self.encounter.encounter_number} | "
                f"{self.patient.full_name} | "
                f"{self.provider.employee.user.get_full_name()}"
            ),
        )

    def test_defaults(
        self,
    ) -> None:
        """
        Default values should be applied.
        """

        encounter = Encounter.objects.create(
            organization=self.organization,
            appointment=self.create_appointment(
                organization=self.organization,
            ),
            patient=self.create_patient(
                organization=self.organization,
                mrn="MRN999999",
            ),
            provider=self.create_provider(
                organization=self.organization,
                provider_number="PRV999999",
                license_number="LIC999999",
            ),
            encounter_number="ENC999999",
        )

        self.assertEqual(
            encounter.status,
            EncounterStatus.SCHEDULED,
        )

        self.assertTrue(
            encounter.is_billable,
        )

        self.assertEqual(
            encounter.duration_minutes,
            0,
        )

    def test_encounter_number(
        self,
    ) -> None:
        """
        Encounter number should be stored correctly.
        """

        self.assertEqual(
            self.encounter.encounter_number,
            "ENC000001",
        )

    def test_status_default(
        self,
    ) -> None:
        """
        Status should default to scheduled.
        """

        self.assertEqual(
            self.encounter.status,
            EncounterStatus.SCHEDULED,
        )

    def test_billable_default(
        self,
    ) -> None:
        """
        Encounter should be billable by default.
        """

        self.assertTrue(
            self.encounter.is_billable,
        )


__all__ = [
    "EncounterModelTestCase",
]
