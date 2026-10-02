from django.core.exceptions import ValidationError

from apps.clinical.medications.constants import MedicationDosageForm, MedicationRoute
from apps.clinical.medications.models import Medication
from apps.common.tests.base import BaseTestCase


class MedicationModelProductionTests(BaseTestCase):
    def create_medication(self, organization=None, **kwargs):
        organization = organization or self.organization
        data = {
            "organization": organization,
            "medication_code": "MED000001",
            "generic_name": "Paracetamol",
            "brand_name": "Crocin",
            "strength": "500",
            "strength_unit": "mg",
            "dosage_form": MedicationDosageForm.TABLET,
            "route": MedicationRoute.ORAL,
            "manufacturer": "ABC Pharma",
            "description": "Pain reliever",
            "is_controlled": False,
        }
        data.update(kwargs)
        return Medication.objects.create(**data)

    def test_display_name(self):
        medication = self.create_medication()
        self.assertEqual(medication.display_name, "Crocin 500 mg")

    def test_soft_delete_deactivates(self):
        medication = self.create_medication()
        medication.soft_delete(getattr(self.admin, "id", None))
        medication.refresh_from_db()
        self.assertTrue(medication.is_deleted)
        self.assertFalse(medication.is_active)

    def test_restore_reactivates(self):
        medication = self.create_medication()
        medication.soft_delete()
        medication.restore()
        medication.refresh_from_db()
        self.assertFalse(medication.is_deleted)
        self.assertTrue(medication.is_active)

    def test_cross_organization_code_allowed(self):
        other = self.create_organization(
            name="Other Organization", code="OTHER", slug="other-organization"
        )
        self.create_medication()
        self.create_medication(organization=other)

    def test_duplicate_code_same_organization_rejected(self):
        self.create_medication()
        with self.assertRaises(Exception):
            self.create_medication()

    def test_deleted_active_state_rejected(self):
        medication = self.create_medication()
        medication.is_deleted = True
        medication.is_active = True
        with self.assertRaises(ValidationError):
            medication.full_clean()
