"""
Tests for the Diagnosis model.
"""

from __future__ import annotations

from apps.common.tests.base import BaseTestCase
from apps.diagnoses.constants import (
    DiagnosisStatus,
    DiagnosisType,
)
from apps.diagnoses.models import Diagnosis
from apps.providers.constants import ProviderType


class DiagnosisModelTestCase(BaseTestCase):
    """
    Test cases for the Diagnosis model.
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

    def test_str(
        self,
    ) -> None:
        """
        String representation should be correct.
        """

        self.assertEqual(
            str(self.diagnosis),
            (
                f"{self.diagnosis.diagnosis_code} | "
                f"{self.diagnosis.diagnosis_description}"
            ),
        )

    def test_defaults(
        self,
    ) -> None:
        """
        Default values should be assigned.
        """

        diagnosis = Diagnosis.objects.create(
            organization=self.organization,
            encounter=self.encounter,
            diagnosis_code="R50.9",
            diagnosis_description="Fever, unspecified",
        )

        self.assertEqual(
            diagnosis.diagnosis_type,
            DiagnosisType.PRIMARY,
        )

        self.assertEqual(
            diagnosis.status,
            DiagnosisStatus.ACTIVE,
        )

        self.assertFalse(
            diagnosis.is_primary,
        )

        self.assertFalse(
            diagnosis.present_on_admission,
        )

        self.assertEqual(
            diagnosis.notes,
            "",
        )


__all__ = [
    "DiagnosisModelTestCase",
]
