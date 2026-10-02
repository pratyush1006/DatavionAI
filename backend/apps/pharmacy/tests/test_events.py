from datetime import timedelta
from decimal import Decimal

from django.test import TestCase
from django.utils import timezone

from apps.pharmacy.models import MedicationBatch, PharmacyOutboxEvent, PharmacyProduct
from apps.pharmacy.services.events import enqueue_event, publish_pending_events
from apps.pharmacy.tests.factories import (
    create_medication,
    create_organization,
    create_pharmacy,
)


class PharmacyEventOutboxTests(TestCase):
    def setUp(self):
        self.organization = create_organization("Event Org")
        self.pharmacy = create_pharmacy(self.organization)
        self.medication = create_medication(self.organization)
        self.product = PharmacyProduct.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            medication=self.medication,
            sku="SKU-EVENT-001",
            selling_price=Decimal("10.00"),
            tax_rate=Decimal("5.000"),
        )
        self.batch = MedicationBatch.objects.create(
            product=self.product,
            batch_number="B-EVENT-001",
            expiry_date=timezone.localdate() + timedelta(days=180),
            quantity_received=Decimal("10"),
            quantity_available=Decimal("10"),
        )

    def test_enqueue_persists_committed_event(self):
        event = enqueue_event(
            organization=self.organization,
            event_type="pharmacy.test",
            aggregate_type="MedicationBatch",
            aggregate_id=self.batch.id,
            payload={"quantity": "2"},
        )
        self.assertEqual(event.status, PharmacyOutboxEvent.Status.PENDING)
        self.assertEqual(PharmacyOutboxEvent.objects.count(), 1)

    def test_publish_marks_event_published_and_delivers_envelope(self):
        event = enqueue_event(
            organization=self.organization,
            event_type="pharmacy.test",
            aggregate_type="MedicationBatch",
            aggregate_id=self.batch.id,
            payload={"quantity": "2"},
        )
        received = []
        count = publish_pending_events(publisher=received.append)
        event.refresh_from_db()
        self.assertEqual(count, 1)
        self.assertEqual(event.status, PharmacyOutboxEvent.Status.PUBLISHED)
        self.assertEqual(received[0]["event_id"], str(event.event_id))
        self.assertEqual(received[0]["payload"], {"quantity": "2"})

    def test_failed_publish_requeues_event(self):
        event = enqueue_event(
            organization=self.organization,
            event_type="pharmacy.test",
            aggregate_type="MedicationBatch",
            aggregate_id=self.batch.id,
        )

        def failing(_):
            raise RuntimeError("broker unavailable")

        self.assertEqual(publish_pending_events(publisher=failing), 0)
        event.refresh_from_db()
        self.assertEqual(event.status, PharmacyOutboxEvent.Status.PENDING)
        self.assertIn("broker unavailable", event.last_error)
        self.assertIsNotNone(event.available_at)

    def test_processing_lease_can_be_reclaimed(self):
        event = enqueue_event(
            organization=self.organization,
            event_type="pharmacy.test",
            aggregate_type="MedicationBatch",
            aggregate_id=self.batch.id,
        )
        event.status = PharmacyOutboxEvent.Status.PROCESSING
        event.locked_until = timezone.now() - timedelta(seconds=1)
        event.save(update_fields=["status", "locked_until", "updated_at"])
        received = []
        self.assertEqual(publish_pending_events(publisher=received.append), 1)
        event.refresh_from_db()
        self.assertEqual(event.status, PharmacyOutboxEvent.Status.PUBLISHED)

    def test_event_created_by_inventory_receipt(self):
        from apps.pharmacy.services.inventory import receive_stock

        receive_stock(
            organization=self.organization, batch=self.batch, quantity=Decimal("2")
        )
        event = PharmacyOutboxEvent.objects.get(event_type="pharmacy.stock_received")
        self.assertEqual(event.aggregate_id, self.batch.id)
        self.assertEqual(event.payload["quantity"], "2")

    def test_event_is_atomic_with_inventory_mutation(self):
        from unittest.mock import patch

        from apps.pharmacy.services.inventory import receive_stock

        with (
            patch(
                "apps.pharmacy.services.inventory.enqueue_event",
                side_effect=RuntimeError("outbox failure"),
            ),
            self.assertRaises(RuntimeError),
        ):
            receive_stock(
                organization=self.organization,
                batch=self.batch,
                quantity=Decimal("2"),
            )
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_available, Decimal("10"))
        self.assertEqual(PharmacyOutboxEvent.objects.count(), 0)
