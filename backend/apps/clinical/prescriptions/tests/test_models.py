"""
Tests for the Prescription model.
"""

from __future__ import annotations

from datetime import date

from apps.clinical.medications.constants import (
    MedicationDosageForm,
    MedicationRoute,
)
from apps.clinical.prescriptions.constants import (
    DEFAULT_PRESCRIPTION_FREQUENCY,
    DEFAULT_PRESCRIPTION_STATUS,
    PrescriptionFrequency,
    PrescriptionStatus,
)
from apps.clinical.prescriptions.models import Prescription
from apps.clinical.providers.constants import ProviderType
from apps.common.tests.base import BaseTestCase


class PrescriptionModelTestCase(BaseTestCase):
    """
    Test cases for the Prescription model.
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

        self.medication = self.create_medication(
            organization=self.organization,
            medication_code="MED000001",
            generic_name="Paracetamol",
            brand_name="Crocin",
            strength="500",
            strength_unit="mg",
            dosage_form=MedicationDosageForm.TABLET,
            route=MedicationRoute.ORAL,
        )

        self.prescription = Prescription.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            encounter=self.encounter,
            medication=self.medication,
            prescription_number="RX000001",
            status=PrescriptionStatus.ACTIVE,
            dosage=1,
            dosage_unit="tablet",
            frequency=PrescriptionFrequency.THREE_TIMES_DAILY,
            quantity=15,
            duration_days=5,
            refills=1,
            start_date=date.today(),
            end_date=date.today(),
            instructions="Take after meals.",
            is_prn=False,
            notes="Initial prescription.",
        )

    def test_str(
        self,
    ) -> None:
        """
        String representation should be correct.
        """

        self.assertEqual(
            str(self.prescription),
            (f"{self.prescription.prescription_number} | {self.prescription.title}"),
        )

    def test_title_property(
        self,
    ) -> None:
        """
        Title property should return a readable title.
        """

        self.assertEqual(
            self.prescription.title,
            (f"{self.medication.title} | {self.patient.full_name}"),
        )

    def test_defaults(
        self,
    ) -> None:
        """
        Default values should be assigned.
        """

        prescription = Prescription.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            encounter=self.encounter,
            medication=self.medication,
            prescription_number="RX000002",
            start_date=date.today(),
            end_date=date.today(),
        )

        self.assertEqual(
            prescription.status,
            DEFAULT_PRESCRIPTION_STATUS,
        )

        self.assertEqual(
            prescription.frequency,
            DEFAULT_PRESCRIPTION_FREQUENCY,
        )

        self.assertEqual(
            prescription.dosage,
            1,
        )

        self.assertEqual(
            prescription.quantity,
            1,
        )

        self.assertEqual(
            prescription.duration_days,
            1,
        )

        self.assertEqual(
            prescription.refills,
            0,
        )

        self.assertFalse(
            prescription.is_prn,
        )

        self.assertEqual(
            prescription.instructions,
            "",
        )

        self.assertEqual(
            prescription.notes,
            "",
        )


__all__ = [
    "PrescriptionModelTestCase",
]
