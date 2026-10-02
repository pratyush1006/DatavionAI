"""
Tests for clinical prescription services.

Prescription deletion is a soft delete:
    - database row remains
    - is_active becomes False
    - is_deleted becomes True
    - deleted_at is populated
    - normal manager hides the row
    - deleted_objects exposes the row
"""

from __future__ import annotations

from datetime import date

from django.core.exceptions import ValidationError

from apps.clinical.appointments.models import Appointment
from apps.clinical.encounters.models import Encounter
from apps.clinical.medications.constants import (
    MedicationDosageForm,
    MedicationRoute,
)
from apps.clinical.prescriptions.constants import (
    PrescriptionFrequency,
    PrescriptionStatus,
)
from apps.clinical.prescriptions.models import Prescription
from apps.clinical.prescriptions.services import (
    PrescriptionService,
    create_prescription,
    delete_prescription,
    update_prescription,
)
from apps.clinical.providers.constants import ProviderType
from apps.common.tests.base import BaseTestCase


class PrescriptionServiceTestCase(BaseTestCase):
    """Prescription service tests."""

    def setUp(self) -> None:
        """Create prescription fixtures."""
        super().setUp()

        self.employee = self.create_employee(
            organization=self.organization,
        )

        self.provider = self.create_provider(
            organization=self.organization,
            employee=self.employee,
            provider_number="PRV000001",
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

    def test_create_prescription(self) -> None:
        """Prescription should be created successfully."""
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
            prescription.patient_id,
            self.patient.pk,
        )
        self.assertEqual(
            prescription.medication_id,
            self.medication.pk,
        )

    def test_update_prescription(self) -> None:
        """Active prescription should be updated."""
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
        self.assertFalse(
            updated.is_deleted,
        )

    def test_delete_prescription_soft_deletes(self) -> None:
        """Prescription delete must be a soft delete."""
        prescription_id = self.prescription.pk

        deleted = delete_prescription(
            instance=self.prescription,
            performed_by=getattr(
                self,
                "user",
                None,
            ),
        )

        self.assertEqual(
            deleted.pk,
            prescription_id,
        )

        persisted = Prescription.all_objects.get(pk=prescription_id)

        self.assertFalse(
            persisted.is_active,
        )
        self.assertTrue(
            persisted.is_deleted,
        )
        self.assertIsNotNone(
            persisted.deleted_at,
        )

        self.assertFalse(
            Prescription.objects.filter(
                pk=prescription_id,
            ).exists(),
        )

        self.assertTrue(
            Prescription.deleted_objects.filter(
                pk=prescription_id,
            ).exists(),
        )

        # all_objects proves the physical row remains.
        self.assertTrue(
            Prescription.all_objects.filter(
                pk=prescription_id,
            ).exists(),
        )

    def test_delete_does_not_physically_delete(self) -> None:
        """Soft deletion must retain the database row."""
        prescription_id = self.prescription.pk

        delete_prescription(
            instance=self.prescription,
        )

        self.assertTrue(
            Prescription.all_objects.filter(
                pk=prescription_id,
            ).exists(),
        )

    def test_update_cannot_modify_soft_deleted_prescription(
        self,
    ) -> None:
        """Soft-deleted prescriptions cannot be updated."""
        prescription_id = self.prescription.pk

        delete_prescription(
            instance=self.prescription,
        )

        with self.assertRaises(ValidationError):
            update_prescription(
                prescription_id=prescription_id,
                organization=self.organization,
                validated_data={
                    "notes": "This update must be rejected.",
                },
            )

    def test_all_prescriptions_must_be_verified_before_auto_checkout(self) -> None:
        from apps.clinical.appointments.constants import AppointmentStatus
        from apps.clinical.encounters.constants import EncounterStatus

        second = Prescription.objects.create(
            organization=self.organization,
            patient=self.patient,
            provider=self.provider,
            encounter=self.encounter,
            medication=self.medication,
            prescription_number="RX000002",
            status=PrescriptionStatus.ACTIVE,
            dosage=1,
            dosage_unit="tablet",
            frequency=PrescriptionFrequency.ONCE_DAILY,
            quantity=5,
            duration_days=5,
            refills=0,
            start_date=date.today(),
            end_date=date.today(),
        )
        Appointment.objects.filter(pk=self.appointment.pk).update(
            status=AppointmentStatus.IN_PROGRESS,
        )
        self.appointment.refresh_from_db()
        Encounter.objects.filter(pk=self.encounter.pk).update(
            status=EncounterStatus.IN_PROGRESS,
        )
        self.encounter.refresh_from_db()
        doctor = self.provider.employee.user

        PrescriptionService.transition(
            organization=self.organization,
            record_id=self.prescription.pk,
            target="verify",
            performed_by=doctor,
        )
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.status, AppointmentStatus.IN_PROGRESS)

        PrescriptionService.transition(
            organization=self.organization,
            record_id=second.pk,
            target="verify",
            performed_by=doctor,
        )
        self.appointment.refresh_from_db()
        self.encounter.refresh_from_db()
        self.assertEqual(self.appointment.status, AppointmentStatus.COMPLETED)
        self.assertIsNotNone(self.appointment.check_out_at)
        self.assertEqual(self.encounter.status, EncounterStatus.COMPLETED)

    def test_create_persists_to_database(self) -> None:
        """Prescription creation must persist."""
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
