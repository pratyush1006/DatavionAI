"""
Tests for prescription API endpoints.
"""

from __future__ import annotations

from datetime import date

from django.urls import reverse
from rest_framework import status

from apps.clinical.medications.constants import (
    MedicationDosageForm,
    MedicationRoute,
)
from apps.clinical.prescriptions.constants import (
    PrescriptionFrequency,
    PrescriptionStatus,
)
from apps.clinical.prescriptions.models import Prescription
from apps.clinical.providers.constants import ProviderType
from apps.common.tests.base import BaseAPITestCase


class PrescriptionAPITestCase(BaseAPITestCase):
    """
    Test cases for prescription API endpoints.
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

        self.list_url = reverse(
            "prescriptions:list-create",
        )

        self.detail_url = reverse(
            "prescriptions:detail",
            kwargs={
                "prescription_id": self.prescription.id,
            },
        )

    def test_list_prescriptions(
        self,
    ) -> None:
        """
        List endpoint should return HTTP 200.
        """

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_retrieve_prescription(
        self,
    ) -> None:
        """
        Detail endpoint should return HTTP 200.
        """

        response = self.client.get(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_prescription(
        self,
    ) -> None:
        """
        Create endpoint should create a prescription.
        """

        payload = {
            "organization": str(self.organization.id),
            "patient": str(self.patient.id),
            "provider": str(self.provider.id),
            "encounter": str(self.encounter.id),
            "medication": str(self.medication.id),
            "prescription_number": "RX000002",
            "status": PrescriptionStatus.ACTIVE,
            "dosage": "2.00",
            "dosage_unit": "tablet",
            "frequency": PrescriptionFrequency.TWICE_DAILY,
            "quantity": "20.00",
            "duration_days": 10,
            "refills": 2,
            "start_date": date.today().isoformat(),
            "end_date": date.today().isoformat(),
            "instructions": "Take after food.",
            "is_prn": False,
            "notes": "Follow-up prescription.",
        }

        response = self.client.post(
            self.list_url,
            payload,
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_201_CREATED,
        )

    def test_create_prescription_validation_error(
        self,
    ) -> None:
        """
        Invalid payload should return HTTP 400.
        """

        response = self.client.post(
            self.list_url,
            {},
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )

    def test_update_prescription(
        self,
    ) -> None:
        """
        PUT endpoint should update the prescription.
        """

        response = self.client.put(
            self.detail_url,
            {
                "organization": str(self.organization.id),
                "patient": str(self.patient.id),
                "provider": str(self.provider.id),
                "encounter": str(self.encounter.id),
                "medication": str(self.medication.id),
                "prescription_number": "RX000001",
                "status": PrescriptionStatus.COMPLETED,
                "dosage": "1.00",
                "dosage_unit": "tablet",
                "frequency": PrescriptionFrequency.ONCE_DAILY,
                "quantity": "15.00",
                "duration_days": 5,
                "refills": 0,
                "start_date": self.prescription.start_date.isoformat(),
                "end_date": self.prescription.end_date.isoformat(),
                "instructions": "Treatment completed.",
                "is_prn": False,
                "notes": "Completed.",
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_partial_update_prescription(
        self,
    ) -> None:
        """
        PATCH endpoint should update part of the prescription.
        """

        response = self.client.patch(
            self.detail_url,
            {
                "status": PrescriptionStatus.CANCELLED,
            },
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_delete_prescription(
        self,
    ) -> None:
        """
        DELETE endpoint should remove the prescription.
        """

        response = self.client.delete(
            self.detail_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT,
        )

    def test_requires_authentication(
        self,
    ) -> None:
        """
        Endpoints should require authentication.
        """

        self.client.force_authenticate(
            user=None,
        )

        response = self.client.get(
            self.list_url,
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )


__all__ = [
    "PrescriptionAPITestCase",
]
