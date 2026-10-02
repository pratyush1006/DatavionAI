from django.test import SimpleTestCase

from apps.clinical.laboratories.models import LaboratoryOutboxEvent


class LaboratoryEventTests(SimpleTestCase):
    def test_outbox_model_exposes_event_contract(self):
        field_names = {field.name for field in LaboratoryOutboxEvent._meta.fields}
        self.assertTrue(
            {"event_type", "payload", "status", "attempts"}.issubset(field_names)
        )
