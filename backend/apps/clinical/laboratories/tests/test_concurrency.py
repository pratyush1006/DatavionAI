from django.test import SimpleTestCase

from apps.clinical.laboratories.models import LaboratorySlot


class LaboratoryConcurrencyTests(SimpleTestCase):
    def test_slot_has_capacity_and_time_constraints(self):
        names = {constraint.name for constraint in LaboratorySlot._meta.constraints}
        self.assertIn("ck_lab_slot_time", names)
        self.assertIn("ck_lab_slot_capacity", names)
