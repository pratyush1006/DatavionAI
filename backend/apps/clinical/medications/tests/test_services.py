from django.core.exceptions import ValidationError

from apps.clinical.medications.constants import MedicationDosageForm, MedicationRoute
from apps.clinical.medications.services import (
    create_medication,
    delete_medication,
    restore_medication,
    update_medication,
)
from apps.common.tests.base import BaseTestCase


class MedicationServiceProductionTests(BaseTestCase):
    def data(self):
        return {
            "medication_code": "MED000001",
            "generic_name": "Paracetamol",
            "brand_name": "Crocin",
            "strength": "500",
            "strength_unit": "mg",
            "dosage_form": MedicationDosageForm.TABLET,
            "route": MedicationRoute.ORAL,
        }

    def test_create_is_tenant_scoped(self):
        medication = create_medication(
            organization=self.organization,
            validated_data=self.data(),
            actor=self.admin,
        )
        self.assertEqual(medication.organization_id, self.organization.id)

    def test_update_cannot_change_organization(self):
        medication = create_medication(
            organization=self.organization,
            validated_data=self.data(),
        )
        other = self.create_organization(
            name="Other Organization", code="OTHER", slug="other-organization"
        )
        with self.assertRaises(ValidationError):
            update_medication(
                instance=medication,
                organization=other,
                validated_data={"generic_name": "Changed"},
            )

    def test_update_persists(self):
        medication = create_medication(
            organization=self.organization,
            validated_data=self.data(),
        )
        update_medication(
            instance=medication,
            organization=self.organization,
            validated_data={"generic_name": "Acetaminophen"},
        )
        medication.refresh_from_db()
        self.assertEqual(medication.generic_name, "Acetaminophen")

    def test_delete_is_soft(self):
        medication = create_medication(
            organization=self.organization,
            validated_data=self.data(),
        )
        delete_medication(
            instance=medication,
            organization=self.organization,
            actor=self.admin,
        )
        medication.refresh_from_db()
        self.assertTrue(medication.is_deleted)
        self.assertFalse(medication.is_active)

    def test_restore(self):
        medication = create_medication(
            organization=self.organization,
            validated_data=self.data(),
        )
        delete_medication(instance=medication, organization=self.organization)
        restore_medication(instance=medication, organization=self.organization)
        medication.refresh_from_db()
        self.assertFalse(medication.is_deleted)
        self.assertTrue(medication.is_active)
