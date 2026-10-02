from unittest.mock import patch

from django.test import SimpleTestCase, TestCase

from apps.clinical.laboratories.models import LaboratoryOutboxEvent
from apps.clinical.laboratories.services.events import (
    event,
    publish_pending_events,
    retry_failed_event,
)
from apps.clinical.laboratories.tests.factories import make_basic_lab_context


class LaboratoryOutboxHardeningTests(TestCase):
    def setUp(self):
        self.ctx = make_basic_lab_context()

    def test_successful_publish(self):
        obj = event(
            self.ctx["organization"].id,
            "laboratory.test",
            "Laboratory",
            self.ctx["laboratory"].id,
            {"ok": True},
        )
        received = []
        self.assertEqual(publish_pending_events(publisher=received.append), 1)
        obj.refresh_from_db()
        self.assertEqual(obj.status, LaboratoryOutboxEvent.Status.PUBLISHED)
        self.assertEqual(received[0]["event_id"], str(obj.event_id))

    def test_failure_reaches_dead_letter_and_can_replay(self):
        obj = event(
            self.ctx["organization"].id,
            "laboratory.test",
            "Laboratory",
            self.ctx["laboratory"].id,
        )
        with patch("apps.clinical.laboratories.services.events.MAX_EVENT_ATTEMPTS", 1):
            publish_pending_events(
                publisher=lambda _: (_ for _ in ()).throw(RuntimeError("broker down"))
            )
        obj.refresh_from_db()
        self.assertEqual(obj.status, LaboratoryOutboxEvent.Status.FAILED)
        self.assertEqual(
            retry_failed_event(
                event_id=obj.event_id, organization_id=self.ctx["organization"].id
            ),
            1,
        )
        obj.refresh_from_db()
        self.assertEqual(obj.status, LaboratoryOutboxEvent.Status.PENDING)


class LaboratoryReadinessContractTests(SimpleTestCase):
    def test_readiness_is_callable(self):
        from apps.clinical.laboratories.services.events import laboratory_readiness

        self.assertTrue(callable(laboratory_readiness))
