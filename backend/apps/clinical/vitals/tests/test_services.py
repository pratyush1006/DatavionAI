"""
Tests for vital services.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.utils import timezone

from apps.clinical.providers.constants import ProviderType
from apps.clinical.vitals.constants import (
    TemperatureUnit,
    VitalStatus,
)
from apps.clinical.vitals.models import Vital
from apps.clinical.vitals.services import (
    create_vital,
    delete_vital,
    update_vital,
)
from apps.common.tests.base import BaseTestCase


class VitalServiceTestCase(BaseTestCase):
    """
    Test cases for vital services.
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
            provider_number="PRV000001",
            license_number="LIC000001",
            provider_type=ProviderType.PHYSICIAN,
        )

        self.patient = self.create_patient(
            organization=self.organization,
            mrn="MRN000001",
            first_name="John",
            last_name="Doe",
        )

        self.appointment = self.create_appointment(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            appointment_number="APT000001",
        )

        self.encounter = self.create_encounter(
            organization=self.organization,
            appointment=self.appointment,
            patient=self.patient,
            provider=self.provider,
            encounter_number="ENC000001",
        )

        self.recorded_at = timezone.now()

        self.vital = Vital.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            encounter=self.encounter,
            recorded_at=self.recorded_at,
            height_cm=Decimal("175.00"),
            weight_kg=Decimal("70.00"),
            bmi=Decimal("22.86"),
            temperature=Decimal("98.6"),
            temperature_unit=TemperatureUnit.FAHRENHEIT,
            pulse=72,
            respiratory_rate=18,
            systolic_bp=120,
            diastolic_bp=80,
            oxygen_saturation=98,
            pain_score=2,
            status=VitalStatus.FINAL,
            notes="Initial vital record.",
        )

    def test_create_vital(
        self,
    ) -> None:
        """
        Vital should be created successfully.
        """

        vital = create_vital(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "encounter": self.encounter,
                "recorded_at": self.recorded_at + timedelta(minutes=1),
                "height_cm": Decimal("180.00"),
                "weight_kg": Decimal("75.00"),
                "bmi": Decimal("23.15"),
                "temperature": Decimal("99.1"),
                "temperature_unit": TemperatureUnit.FAHRENHEIT,
                "pulse": 75,
                "respiratory_rate": 16,
                "systolic_bp": 118,
                "diastolic_bp": 78,
                "oxygen_saturation": 99,
                "pain_score": 1,
                "status": VitalStatus.FINAL,
                "notes": "Follow-up vital record.",
            },
        )

        self.assertIsInstance(
            vital,
            Vital,
        )

        self.assertEqual(
            vital.patient,
            self.patient,
        )

        self.assertEqual(
            vital.provider,
            self.provider,
        )

        self.assertEqual(
            vital.temperature,
            Decimal("99.1"),
        )

    def test_update_vital(
        self,
    ) -> None:
        """
        Vital should be updated successfully.
        """

        updated = update_vital(
            instance=self.vital,
            validated_data={
                "pulse": 80,
                "status": VitalStatus.FINAL,
                "notes": "Updated vital record.",
            },
        )

        updated.refresh_from_db()

        self.assertEqual(
            updated.pulse,
            80,
        )

        self.assertEqual(
            updated.status,
            VitalStatus.FINAL,
        )

        self.assertEqual(
            updated.notes,
            "Updated vital record.",
        )

    def test_delete_vital(
        self,
    ) -> None:
        """
        Vital should be deleted successfully.
        """

        vital_id = self.vital.id

        delete_vital(
            instance=self.vital,
        )

        self.assertFalse(
            Vital.objects.filter(
                id=vital_id,
            ).exists(),
        )

    def test_update_returns_same_instance(
        self,
    ) -> None:
        """
        Update service should return the same instance.
        """

        updated = update_vital(
            instance=self.vital,
            validated_data={
                "oxygen_saturation": 100,
            },
        )

        self.assertEqual(
            updated.pk,
            self.vital.pk,
        )

        self.assertEqual(
            updated.oxygen_saturation,
            100,
        )

    def test_create_persists_to_database(
        self,
    ) -> None:
        """
        Vital should persist after creation.
        """

        initial_count = Vital.objects.count()

        create_vital(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "encounter": self.encounter,
                "recorded_at": self.recorded_at + timedelta(minutes=2),
            },
        )

        self.assertEqual(
            Vital.objects.count(),
            initial_count + 1,
        )


__all__ = [
    "VitalServiceTestCase",
]
