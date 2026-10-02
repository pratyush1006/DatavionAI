from django.test import SimpleTestCase

from apps.clinical.laboratories.models import LaboratoryOrder


class LaboratoryEnterpriseHardeningTests(SimpleTestCase):
    def test_order_has_organization_scope(self):
        self.assertIsNotNone(LaboratoryOrder._meta.get_field("organization"))

    def test_order_has_canonical_patient_and_appointment_contracts(self):
        self.assertEqual(
            LaboratoryOrder._meta.get_field(
                "appointment"
            ).remote_field.model._meta.label_lower,
            "appointments.appointment",
        )
        self.assertEqual(
            LaboratoryOrder._meta.get_field(
                "patient"
            ).remote_field.model._meta.label_lower,
            "patient_core.patient",
        )
