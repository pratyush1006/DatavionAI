"""
Tests for encounter services.
"""

from __future__ import annotations

from datetime import timedelta

from django.utils import timezone

from apps.clinical.encounters.constants import (
    EncounterStatus,
)
from apps.clinical.encounters.models import Encounter
from apps.clinical.encounters.services import (
    create_encounter,
    delete_encounter,
    update_encounter,
)
from apps.common.tests.base import BaseTestCase


class EncounterServiceTestCase(
    BaseTestCase,
):
    """
    Test encounter service functions.
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

    def test_create_encounter(
        self,
    ) -> None:
        """
        create_encounter should create a new encounter.
        """

        encounter = create_encounter(
            validated_data={
                "organization": self.organization,
                "appointment": self.appointment,
                "patient": self.patient,
                "provider": self.provider,
                "encounter_number": "ENC000001",
                "status": EncounterStatus.SCHEDULED,
                "chief_complaint": "Fever",
                "started_at": timezone.now(),
                "ended_at": timezone.now()
                + timedelta(
                    minutes=20,
                ),
                "duration_minutes": 20,
                "is_billable": True,
            },
        )

        self.assertIsInstance(
            encounter,
            Encounter,
        )

        self.assertEqual(
            encounter.encounter_number,
            "ENC000001",
        )

    def test_update_encounter(
        self,
    ) -> None:
        """
        update_encounter should update an encounter.
        """

        encounter = Encounter.objects.create(
            organization=self.organization,
            appointment=self.appointment,
            patient=self.patient,
            provider=self.provider,
            encounter_number="ENC000001",
            status=EncounterStatus.SCHEDULED,
        )

        encounter = update_encounter(
            instance=encounter,
            validated_data={
                "status": EncounterStatus.COMPLETED,
                "chief_complaint": "Updated complaint",
            },
        )

        self.assertEqual(
            encounter.status,
            EncounterStatus.COMPLETED,
        )

        self.assertEqual(
            encounter.chief_complaint,
            "Updated complaint",
        )

    def test_delete_encounter(
        self,
    ) -> None:
        """
        delete_encounter should delete an encounter.
        """

        encounter = Encounter.objects.create(
            organization=self.organization,
            appointment=self.appointment,
            patient=self.patient,
            provider=self.provider,
            encounter_number="ENC000001",
            status=EncounterStatus.SCHEDULED,
        )

        encounter_id = encounter.id

        delete_encounter(
            instance=encounter,
        )

        self.assertFalse(
            Encounter.objects.filter(
                id=encounter_id,
            ).exists(),
        )


__all__ = [
    "EncounterServiceTestCase",
]
