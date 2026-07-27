"""
Tests for patient services.
"""

from __future__ import annotations

from datetime import date

from django.core.exceptions import ValidationError

from apps.clinical.patients.constants import (
    PatientGender,
    PatientStatus,
)
from apps.clinical.patients.models import Patient
from apps.clinical.patients.services import PatientService
from apps.clinical.patients.tests.factories import PatientFactory
from apps.common.tests.base import BaseTestCase


class PatientServiceTestCase(BaseTestCase):
    """
    Test cases for PatientService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = PatientFactory(
            organization=self.organization,
            mrn="MRN000001",
            first_name="John",
            last_name="Doe",
            date_of_birth=date(
                1995,
                5,
                20,
            ),
            gender=PatientGender.MALE,
        )

    def test_create_patient(self) -> None:
        """
        Patient should be created successfully.
        """

        patient = PatientService.create(
            validated_data={
                "organization": self.organization,
                "mrn": "MRN000002",
                "first_name": "Jane",
                "last_name": "Smith",
                "date_of_birth": date(
                    1998,
                    8,
                    15,
                ),
                "gender": PatientGender.FEMALE,
                "status": PatientStatus.ACTIVE,
            },
        )

        self.assertIsInstance(
            patient,
            Patient,
        )

        self.assertEqual(
            patient.organization,
            self.organization,
        )

        self.assertEqual(
            patient.mrn,
            "MRN000002",
        )

        self.assertEqual(
            patient.first_name,
            "Jane",
        )

        self.assertEqual(
            patient.last_name,
            "Smith",
        )

    def test_create_patient_persists_to_database(self) -> None:
        """
        Created patient should be persisted.
        """

        initial_count = Patient.objects.count()

        PatientService.create(
            validated_data={
                "organization": self.organization,
                "mrn": "MRN000003",
                "first_name": "Alice",
                "last_name": "Brown",
                "date_of_birth": date(
                    2000,
                    1,
                    1,
                ),
                "gender": PatientGender.FEMALE,
                "status": PatientStatus.ACTIVE,
            },
        )

        self.assertEqual(
            Patient.objects.count(),
            initial_count + 1,
        )

    def test_create_duplicate_mrn_raises_error(self) -> None:
        """
        Duplicate MRN within an organization should fail.
        """

        with self.assertRaises(
            ValidationError,
        ):
            PatientService.create(
                validated_data={
                    "organization": self.organization,
                    "mrn": "MRN000001",
                    "first_name": "Duplicate",
                    "last_name": "Patient",
                    "date_of_birth": date(
                        1990,
                        1,
                        1,
                    ),
                    "gender": PatientGender.MALE,
                },
            )

    def test_update_patient(self) -> None:
        """
        Patient should be updated successfully.
        """

        updated_patient = PatientService.update(
            instance=self.patient,
            validated_data={
                "first_name": "Jonathan",
                "status": PatientStatus.INACTIVE,
            },
        )

        updated_patient.refresh_from_db()

        self.assertEqual(
            updated_patient.first_name,
            "Jonathan",
        )

        self.assertEqual(
            updated_patient.status,
            PatientStatus.INACTIVE,
        )

    def test_update_patient_returns_same_instance(self) -> None:
        """
        Update should return the same patient instance.
        """

        updated_patient = PatientService.update(
            instance=self.patient,
            validated_data={
                "last_name": "Williams",
            },
        )

        self.assertEqual(
            updated_patient.pk,
            self.patient.pk,
        )

        self.assertEqual(
            updated_patient.last_name,
            "Williams",
        )

    def test_delete_patient(self) -> None:
        """
        Patient should be deleted successfully.
        """

        patient_id = self.patient.pk

        PatientService.delete(
            instance=self.patient,
        )

        self.assertFalse(
            Patient.objects.filter(
                pk=patient_id,
            ).exists(),
        )

    def test_archive_patient(self) -> None:
        """
        Patient should be archived successfully.
        """

        archived_patient = PatientService.archive(
            instance=self.patient,
        )

        archived_patient.refresh_from_db()

        self.assertFalse(
            archived_patient.is_active,
        )

    def test_restore_patient(self) -> None:
        """
        Archived patient should be restored successfully.
        """

        PatientService.archive(
            instance=self.patient,
        )

        restored_patient = PatientService.restore(
            instance=self.patient,
        )

        restored_patient.refresh_from_db()

        self.assertTrue(
            restored_patient.is_active,
        )

    def test_create_patient_invalid_phone_raises_validation_error(
        self,
    ) -> None:
        """
        Invalid phone number should fail validation.
        """

        with self.assertRaises(
            ValidationError,
        ):
            PatientService.create(
                validated_data={
                    "organization": self.organization,
                    "mrn": "MRN000010",
                    "first_name": "Jane",
                    "last_name": "Smith",
                    "phone": "123",
                    "date_of_birth": date(
                        1999,
                        1,
                        1,
                    ),
                    "gender": PatientGender.FEMALE,
                },
            )


__all__ = [
    "PatientServiceTestCase",
]
