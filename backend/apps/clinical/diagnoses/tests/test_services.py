"""
Tests for diagnosis services.
"""

from __future__ import annotations

from apps.clinical.diagnoses.constants import (
    DiagnosisStatus,
    DiagnosisType,
)
from apps.clinical.diagnoses.models import Diagnosis
from apps.clinical.diagnoses.services import (
    create_diagnosis,
    delete_diagnosis,
    update_diagnosis,
)
from apps.common.tests.base import BaseTestCase


class DiagnosisServiceTestCase(BaseTestCase):
    """
    Test cases for diagnosis services.
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

        self.encounter = self.create_encounter(
            organization=self.organization,
            appointment=self.appointment,
            patient=self.patient,
            provider=self.provider,
        )

        self.diagnosis = Diagnosis.objects.create(
            organization=self.organization,
            encounter=self.encounter,
            diagnosis_code="J10.1",
            diagnosis_description="Influenza with pneumonia",
            diagnosis_type=DiagnosisType.PRIMARY,
            status=DiagnosisStatus.ACTIVE,
            is_primary=True,
            present_on_admission=True,
            notes="Initial diagnosis.",
        )

    def test_create_diagnosis(
        self,
    ) -> None:
        """
        Diagnosis should be created successfully.
        """

        diagnosis = create_diagnosis(
            validated_data={
                "organization": self.organization,
                "encounter": self.encounter,
                "diagnosis_code": "R50.9",
                "diagnosis_description": "Fever, unspecified",
                "diagnosis_type": DiagnosisType.SECONDARY,
                "status": DiagnosisStatus.ACTIVE,
                "is_primary": False,
                "present_on_admission": False,
                "notes": "Secondary diagnosis.",
            },
        )

        self.assertIsInstance(
            diagnosis,
            Diagnosis,
        )

        self.assertEqual(
            diagnosis.diagnosis_code,
            "R50.9",
        )

        self.assertEqual(
            diagnosis.encounter,
            self.encounter,
        )

    def test_update_diagnosis(
        self,
    ) -> None:
        """
        Diagnosis should be updated successfully.
        """

        updated = update_diagnosis(
            instance=self.diagnosis,
            validated_data={
                "status": DiagnosisStatus.RESOLVED,
                "notes": "Patient recovered.",
                "is_primary": False,
            },
        )

        updated.refresh_from_db()

        self.assertEqual(
            updated.status,
            DiagnosisStatus.RESOLVED,
        )

        self.assertEqual(
            updated.notes,
            "Patient recovered.",
        )

        self.assertFalse(
            updated.is_primary,
        )

    def test_delete_diagnosis(
        self,
    ) -> None:
        """
        Diagnosis should be deleted successfully.
        """

        diagnosis_id = self.diagnosis.id

        delete_diagnosis(
            instance=self.diagnosis,
        )

        self.assertFalse(
            Diagnosis.objects.filter(
                id=diagnosis_id,
            ).exists(),
        )

    def test_update_returns_same_instance(
        self,
    ) -> None:
        """
        Update service should return the same instance.
        """

        updated = update_diagnosis(
            instance=self.diagnosis,
            validated_data={
                "status": DiagnosisStatus.INACTIVE,
            },
        )

        self.assertEqual(
            updated.pk,
            self.diagnosis.pk,
        )

        self.assertEqual(
            updated.status,
            DiagnosisStatus.INACTIVE,
        )

    def test_create_persists_to_database(
        self,
    ) -> None:
        """
        Diagnosis should persist after creation.
        """

        initial_count = Diagnosis.objects.count()

        create_diagnosis(
            validated_data={
                "organization": self.organization,
                "encounter": self.encounter,
                "diagnosis_code": "E11.9",
                "diagnosis_description": "Type 2 diabetes mellitus",
                "diagnosis_type": DiagnosisType.SECONDARY,
            },
        )

        self.assertEqual(
            Diagnosis.objects.count(),
            initial_count + 1,
        )


__all__ = [
    "DiagnosisServiceTestCase",
]
