from rest_framework import status
from rest_framework.test import APIClient

from apps.clinical.medications.constants import MedicationDosageForm, MedicationRoute
from apps.clinical.medications.models import Medication
from apps.common.tests.base import BaseTestCase


class MedicationAPITestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin)
        self.list_url = "/api/medications/"
        self.medication = Medication.objects.create(
            organization=self.organization,
            medication_code="MED-API-001",
            generic_name="Paracetamol",
            brand_name="Crocin",
            strength="500",
            strength_unit="mg",
            dosage_form=MedicationDosageForm.TABLET,
            route=MedicationRoute.ORAL,
        )
        self.detail_url = f"/api/medications/{self.medication.id}/"

    def payload(self):
        return {
            "medication_code": "MED-API-002",
            "generic_name": "Ibuprofen",
            "brand_name": "Brufen",
            "strength": "400",
            "strength_unit": "mg",
            "dosage_form": MedicationDosageForm.TABLET,
            "route": MedicationRoute.ORAL,
        }

    def test_list_medications(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_medication(self):
        response = self.client.post(self.list_url, self.payload(), format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(
            Medication.objects.filter(
                organization=self.organization,
                medication_code="MED-API-002",
            ).exists()
        )

    def test_create_medication_validation_error(self):
        payload = self.payload()
        payload["generic_name"] = ""
        response = self.client.post(self.list_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_medication(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_medication(self):
        payload = self.payload()
        payload["medication_code"] = self.medication.medication_code
        response = self.client.put(self.detail_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_partial_update_medication(self):
        response = self.client.patch(
            self.detail_url,
            {"generic_name": "Acetaminophen"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_medication(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.medication.refresh_from_db()
        self.assertTrue(self.medication.is_deleted)

    def test_requires_authentication(self):
        self.client.force_authenticate(user=None)
        response = self.client.get(self.list_url)
        self.assertEqual(
            response.status_code,
            status.HTTP_401_UNAUTHORIZED,
        )
