from apps.clinical.medications.models import Medication
from apps.clinical.medications.selectors import (
    get_medication,
    medication_queryset,
    search_medications,
)
from apps.common.tests.base import BaseTestCase


class MedicationSelectorProductionTests(BaseTestCase):
    def medication(self, organization, code):
        return Medication.objects.create(
            organization=organization,
            medication_code=code,
            generic_name="Paracetamol",
            brand_name="Crocin",
            strength="500",
            strength_unit="mg",
            dosage_form="tablet",
            route="oral",
        )

    def test_queryset_is_tenant_scoped(self):
        other = self.create_organization(
            name="Other Organization", code="OTHER", slug="other-organization"
        )
        mine = self.medication(self.organization, "MED1")
        self.medication(other, "MED2")
        self.assertEqual(
            list(medication_queryset(organization=self.organization)), [mine]
        )

    def test_search_by_generic_name(self):
        medication = self.medication(self.organization, "MED1")
        result = list(
            search_medications(organization=self.organization, query="paracetamol")
        )
        self.assertEqual(result, [medication])

    def test_get_medication_returns_owned_record(self):
        medication = self.medication(self.organization, "MED1")
        self.assertEqual(
            get_medication(
                organization=self.organization,
                medication_id=medication.id,
            ).id,
            medication.id,
        )
