"""
Tests for prescription services.
"""

from __future__ import annotations

from datetime import date

from apps.common.tests.base import BaseTestCase
from apps.medications.constants import (
    MedicationDosageForm,
    MedicationRoute,
)
from apps.prescriptions.constants import (
    PrescriptionFrequency,
    PrescriptionStatus,
)
from apps.prescriptions.models import Prescription
from apps.prescriptions.services import (
    create_prescription,
    delete_prescription,
    update_prescription,
)
from apps.providers.constants import ProviderType


class PrescriptionServiceTestCase(BaseTestCase):
    """
    Test cases for prescription services.
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

    def test_create_prescription(
        self,
    ) -> None:
        """
        Prescription should be created successfully.
        """

        prescription = create_prescription(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "encounter": self.encounter,
                "medication": self.medication,
                "prescription_number": "RX000002",
                "status": PrescriptionStatus.ACTIVE,
                "dosage": 2,
                "dosage_unit": "tablet",
                "frequency": PrescriptionFrequency.TWICE_DAILY,
                "quantity": 20,
                "duration_days": 10,
                "refills": 2,
                "start_date": date.today(),
                "end_date": date.today(),
                "instructions": "After food.",
                "is_prn": False,
                "notes": "Follow-up prescription.",
            },
        )

        self.assertIsInstance(
            prescription,
            Prescription,
        )

        self.assertEqual(
            prescription.prescription_number,
            "RX000002",
        )

        self.assertEqual(
            prescription.patient,
            self.patient,
        )

        self.assertEqual(
            prescription.medication,
            self.medication,
        )

    def test_update_prescription(
        self,
    ) -> None:
        """
        Prescription should be updated successfully.
        """

        updated = update_prescription(
            instance=self.prescription,
            validated_data={
                "status": PrescriptionStatus.COMPLETED,
                "refills": 0,
                "notes": "Treatment completed.",
            },
        )

        updated.refresh_from_db()

        self.assertEqual(
            updated.status,
            PrescriptionStatus.COMPLETED,
        )

        self.assertEqual(
            updated.refills,
            0,
        )

        self.assertEqual(
            updated.notes,
            "Treatment completed.",
        )

    def test_delete_prescription(
        self,
    ) -> None:
        """
        Prescription should be deleted successfully.
        """

        prescription_id = self.prescription.id

        delete_prescription(
            instance=self.prescription,
        )

        self.assertFalse(
            Prescription.objects.filter(
                id=prescription_id,
            ).exists(),
        )

    def test_update_returns_same_instance(
        self,
    ) -> None:
        """
        Update service should return the same instance.
        """

        updated = update_prescription(
            instance=self.prescription,
            validated_data={
                "duration_days": 14,
            },
        )

        self.assertEqual(
            updated.pk,
            self.prescription.pk,
        )

        self.assertEqual(
            updated.duration_days,
            14,
        )

    def test_create_persists_to_database(
        self,
    ) -> None:
        """
        Prescription should persist after creation.
        """

        initial_count = Prescription.objects.count()

        create_prescription(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "provider": self.provider,
                "encounter": self.encounter,
                "medication": self.medication,
                "prescription_number": "RX000003",
                "start_date": date.today(),
                "end_date": date.today(),
            },
        )

        self.assertEqual(
            Prescription.objects.count(),
            initial_count + 1,
        )


__all__ = [
    "PrescriptionServiceTestCase",
]
