from datetime import timedelta
from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from apps.pharmacy.models import MedicationBatch, PharmacyOutboxEvent, PharmacyProduct
from apps.pharmacy.selectors.events import outbox_summary
from apps.pharmacy.services.events import (
    enqueue_event,
    publish_pending_events,
    retry_failed_event,
)
from apps.pharmacy.services.health import pharmacy_health
from apps.pharmacy.tests.factories import (
    create_medication,
    create_organization,
    create_pharmacy,
)


class PharmacyProductionReadinessTests(TestCase):
    def setUp(self):
        self.organization = create_organization("Production Readiness Org")
        self.pharmacy = create_pharmacy(self.organization)
        self.medication = create_medication(self.organization)
        self.product = PharmacyProduct.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            medication=self.medication,
            sku="SKU-PROD-001",
            selling_price=Decimal("10.00"),
            tax_rate=Decimal("5.000"),
        )
        self.batch = MedicationBatch.objects.create(
            product=self.product,
            batch_number="B-PROD-001",
            expiry_date=timezone.localdate() + timedelta(days=180),
            quantity_received=Decimal("10"),
            quantity_available=Decimal("10"),
        )

    def test_health_reports_database_and_outbox(self):
        payload = pharmacy_health(organization=self.organization)
        self.assertEqual(payload["checks"]["database"]["status"], "ok")
        self.assertEqual(payload["checks"]["outbox"]["status"], "ok")

    def test_outbox_summary_tracks_failed_events(self):
        enqueue_event(
            organization=self.organization,
            event_type="pharmacy.production_test",
            aggregate_type="MedicationBatch",
            aggregate_id=self.batch.id,
        )
        summary = outbox_summary(organization=self.organization)
        self.assertEqual(summary["pending"], 1)
        self.assertEqual(summary["failed"], 0)

    def test_failed_event_moves_to_dead_letter_after_max_attempts(self):
        event = enqueue_event(
            organization=self.organization,
            event_type="pharmacy.production_test",
            aggregate_type="MedicationBatch",
            aggregate_id=self.batch.id,
        )
        with patch("apps.pharmacy.services.events.MAX_EVENT_ATTEMPTS", 1):
            publish_pending_events(
                publisher=lambda _: (_ for _ in ()).throw(RuntimeError("broker down"))
            )
        event.refresh_from_db()
        self.assertEqual(event.status, PharmacyOutboxEvent.Status.FAILED)
        self.assertEqual(event.attempts, 1)
        self.assertEqual(retry_failed_event(event_id=event.event_id), 1)
        event.refresh_from_db()
        self.assertEqual(event.status, PharmacyOutboxEvent.Status.PENDING)

    def test_published_event_is_not_reprocessed(self):
        event = enqueue_event(
            organization=self.organization,
            event_type="pharmacy.production_test",
            aggregate_type="MedicationBatch",
            aggregate_id=self.batch.id,
        )
        received = []
        self.assertEqual(publish_pending_events(publisher=received.append), 1)
        self.assertEqual(publish_pending_events(publisher=received.append), 0)
        self.assertEqual(len(received), 1)
