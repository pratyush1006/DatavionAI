from uuid import uuid4

from django.test import TestCase, override_settings

from apps.imaging.models import ImagingIdempotencyKey, ImagingOutboxEvent
from apps.imaging.services.events import enqueue_event, publish_pending_events
from apps.imaging.services.idempotency import execute_idempotent
from apps.imaging.services.production_readiness import production_readiness_report


class ImagingEnterpriseHardeningTests(TestCase):
    def test_outbox_publish(self):
        e = enqueue_event(
            tenant_id=uuid4(), event_type="imaging.test", aggregate_type="ImagingStudy"
        )
        self.assertEqual(publish_pending_events(publisher=lambda _: None), 1)
        e.refresh_from_db()
        self.assertEqual(e.status, ImagingOutboxEvent.Status.PUBLISHED)

    def test_idempotency(self):
        tenant = uuid4()
        calls = []

        def cb():
            calls.append(1)
            return {"ok": True}, 201

        execute_idempotent(
            tenant_id=tenant, key="k1", operation="study.create", callback=cb
        )
        second = execute_idempotent(
            tenant_id=tenant, key="k1", operation="study.create", callback=cb
        )
        self.assertTrue(second[2])
        self.assertEqual(calls, [1])
        self.assertEqual(
            ImagingIdempotencyKey.objects.filter(tenant_id=tenant).count(), 1
        )

    @override_settings(
        DEBUG=True,
        REDIS_URL="",
        IMAGING_EVENT_PUBLISHER="",
        ALLOWED_HOSTS=["example.com"],
        SESSION_COOKIE_SECURE=False,
        CSRF_COOKIE_SECURE=False,
    )
    def test_readiness(self):
        report = production_readiness_report()
        self.assertEqual(report["status"], "not_ready")
        self.assertFalse(report["checks"]["debug_disabled"]["ok"])
        self.assertFalse(report["checks"]["redis"]["ok"])
