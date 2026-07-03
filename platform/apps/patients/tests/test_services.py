"""
Tests for patient services.
"""

from __future__ import annotations

from datetime import date

from apps.common.tests.base import BaseTestCase
from apps.patients.constants import (
    PatientGender,
    PatientStatus,
)
from apps.patients.models import Patient
from apps.patients.services import (
    create_patient,
    delete_patient,
    update_patient,
)


class PatientServiceTestCase(BaseTestCase):
    """
    Test cases for patient services.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.patient = Patient.objects.create(
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

    def test_create_patient(
        self,
    ) -> None:
        """
        Patient should be created successfully.
        """

        patient = create_patient(
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

    def test_update_patient(
        self,
    ) -> None:
        """
        Patient should be updated successfully.
        """

        updated_patient = update_patient(
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

    def test_delete_patient(
        self,
    ) -> None:
        """
        Patient should be deleted successfully.
        """

        patient_id = self.patient.id

        delete_patient(
            instance=self.patient,
        )

        self.assertFalse(
            Patient.objects.filter(
                id=patient_id,
            ).exists(),
        )

    def test_update_patient_returns_same_instance(
        self,
    ) -> None:
        """
        Update service should return the updated patient.
        """

        updated_patient = update_patient(
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

    def test_create_patient_persists_to_database(
        self,
    ) -> None:
        """
        Created patient should be persisted.
        """

        initial_count = Patient.objects.count()

        create_patient(
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


__all__ = [
    "PatientServiceTestCase",
]
