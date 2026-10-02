from django.test import SimpleTestCase

from apps.clinical.laboratories.models import LaboratoryOrder, LaboratoryOutboxEvent


class LaboratoryContractTests(SimpleTestCase):
    def test_order_is_not_a_duplicate_appointment_domain(self):
        self.assertNotEqual(LaboratoryOrder.__name__, "LaboratoryAppointment")
        self.assertIsNotNone(LaboratoryOrder._meta.get_field("appointment"))

    def test_outbox_is_tenant_scoped(self):
        self.assertIsNotNone(LaboratoryOutboxEvent._meta.get_field("organization"))
