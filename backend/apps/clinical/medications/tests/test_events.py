from apps.clinical.medications.models import MedicationOutboxEvent
from apps.clinical.medications.services.events import (
    enqueue_event,
    publish_pending_events,
)
from apps.common.tests.base import BaseTestCase


class MedicationEventTests(BaseTestCase):
    def test_enqueue_event(self):
        event = enqueue_event(
            organization=self.organization,
            event_type="medication.test",
            aggregate_type="Medication",
            payload={"ok": True},
        )
        self.assertEqual(event.status, MedicationOutboxEvent.Status.PENDING)

    def test_publish_requires_publisher(self):
        enqueue_event(
            organization=self.organization,
            event_type="medication.test",
            aggregate_type="Medication",
        )
        self.assertEqual(publish_pending_events(limit=1, publisher=None), 0)
        event = MedicationOutboxEvent.objects.get()
        self.assertIn(
            event.status,
            {MedicationOutboxEvent.Status.PENDING, MedicationOutboxEvent.Status.FAILED},
        )
