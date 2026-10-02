from concurrent.futures import ThreadPoolExecutor
from datetime import timedelta
from decimal import Decimal
from threading import Barrier
from unittest.mock import patch

from django.apps import apps
from django.core.exceptions import ValidationError
from django.db import close_old_connections, connection
from django.test import TestCase, TransactionTestCase, skipUnlessDBFeature
from django.utils import timezone

from apps.pharmacy.models import (
    DispensingOrder,
    InventoryReservation,
    MedicationBatch,
    PharmacyBillingRecord,
    PharmacyProduct,
    ProcurementApproval,
    PurchaseOrder,
    StockMovement,
    Supplier,
)
from apps.pharmacy.services.billing import create_dispensing_bill
from apps.pharmacy.services.dispensing import dispense_order
from apps.pharmacy.services.idempotency import execute_idempotent
from apps.pharmacy.services.inventory import receive_stock
from apps.pharmacy.services.procurement import (
    decide_purchase_approval,
    request_purchase_approval,
)
from apps.pharmacy.services.reservations import (
    commit_reservation,
    release_reservation,
    reserve_stock,
)
from apps.pharmacy.tests.factories import (
    create_medication,
    create_organization,
    create_pharmacy,
    create_prescription,
    create_user,
)


class PharmacyTransactionRollbackTests(TestCase):
    def setUp(self):
        self.organization = create_organization("Concurrency Rollback Org")
        self.pharmacy = create_pharmacy(self.organization)
        self.medication = create_medication(self.organization)
        self.product = PharmacyProduct.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            medication=self.medication,
            sku="SKU-TX-001",
            selling_price=Decimal("10.00"),
            tax_rate=Decimal("5.000"),
        )
        self.batch = MedicationBatch.objects.create(
            product=self.product,
            batch_number="B-TX-001",
            expiry_date=timezone.localdate() + timedelta(days=180),
            quantity_received=Decimal("10"),
            quantity_available=Decimal("10"),
        )

    def test_inventory_mutation_rolls_back_when_movement_write_fails(self):
        with (
            patch(
                "apps.pharmacy.services.inventory.StockMovement.objects.create",
                side_effect=RuntimeError("movement failure"),
            ),
            self.assertRaises(RuntimeError),
        ):
            receive_stock(
                organization=self.organization,
                batch=self.batch,
                quantity=Decimal("5"),
                reference_type="rollback-test",
            )
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_received, Decimal("10"))
        self.assertEqual(self.batch.quantity_available, Decimal("10"))
        self.assertFalse(
            StockMovement.objects.filter(reference_type="rollback-test").exists()
        )


@skipUnlessDBFeature("supports_transactions")
class PharmacyConcurrencyTests(TransactionTestCase):
    reset_sequences = True

    def setUp(self):
        if connection.vendor == "sqlite":
            self.skipTest(
                "SQLite cannot provide the row-locking concurrency guarantees required by v1.6 tests."
            )
        self.organization = create_organization("Concurrency Org")
        self.pharmacy = create_pharmacy(self.organization)
        self.medication = create_medication(self.organization)
        self.product = PharmacyProduct.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            medication=self.medication,
            sku="SKU-CONC-001",
            selling_price=Decimal("10.00"),
            tax_rate=Decimal("5.000"),
        )
        self.user = create_user(self.organization)
        self.batch = MedicationBatch.objects.create(
            product=self.product,
            batch_number="B-CONC-001",
            expiry_date=timezone.localdate() + timedelta(days=180),
            quantity_received=Decimal("10"),
            quantity_available=Decimal("10"),
        )

    def _parallel(self, fn, count=2):
        barrier = Barrier(count)

        def wrapped():
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                return fn()
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=count) as pool:
            return list(pool.map(lambda _: wrapped(), range(count)))

    def test_concurrent_dispensing_cannot_overdraw_same_batch(self):
        prescription = create_prescription(self.organization)
        prescription.medication = self.medication
        prescription.status = "active"
        prescription.quantity = Decimal("10")
        prescription.refills = 0
        prescription.start_date = timezone.localdate()
        prescription.end_date = timezone.localdate() + timedelta(days=2)
        prescription.save()
        orders = [
            DispensingOrder.objects.create(
                organization=self.organization,
                pharmacy=self.pharmacy,
                prescription=prescription,
                dispense_number=f"CONC-DISP-{i}",
            )
            for i in range(2)
        ]

        def attempt(order_id):
            order = DispensingOrder.objects.get(pk=order_id)
            try:
                dispense_order(
                    organization=self.organization,
                    order=order,
                    pharmacist_id=self.user.id,
                    requested_lines=[
                        {
                            "product": PharmacyProduct.objects.get(pk=self.product.pk),
                            "quantity": Decimal("6"),
                        }
                    ],
                )
                return "ok"
            except ValidationError:
                return "rejected"

        barrier = Barrier(2)

        def worker(order_id):
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                return attempt(order_id)
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(worker, [o.id for o in orders]))
        self.batch.refresh_from_db()
        self.assertEqual(sorted(results), ["ok", "rejected"])
        self.assertGreaterEqual(self.batch.quantity_available, Decimal("0"))
        self.assertEqual(
            DispensingOrder.objects.filter(
                prescription=prescription, status="dispensed"
            ).count(),
            1,
        )

    def test_concurrent_receipts_preserve_both_updates(self):
        def receive():
            batch = MedicationBatch.objects.get(pk=self.batch.pk)
            receive_stock(
                organization=self.organization,
                batch=batch,
                quantity=Decimal("5"),
                reference_type="concurrent-receipt",
            )
            return "ok"

        results = self._parallel(receive)
        self.assertEqual(sorted(results), ["ok", "ok"])
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_received, Decimal("20"))
        self.assertEqual(self.batch.quantity_available, Decimal("20"))

    def test_concurrent_reservations_cannot_overreserve_batch(self):
        def reserve():
            try:
                reserve_stock(
                    organization=self.organization,
                    batch=MedicationBatch.objects.get(pk=self.batch.pk),
                    quantity=Decimal("6"),
                    ttl_minutes=60,
                )
                return "ok"
            except ValidationError:
                return "rejected"

        results = self._parallel(reserve)
        self.assertEqual(sorted(results), ["ok", "rejected"])
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_reserved, Decimal("6"))

    def test_concurrent_commit_and_release_leave_no_reserved_stock(self):
        reservation = reserve_stock(
            organization=self.organization,
            batch=self.batch,
            quantity=Decimal("4"),
            ttl_minutes=60,
        )
        reservation_id = reservation.id
        barrier = Barrier(2)

        def commit():
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                commit_reservation(
                    organization=self.organization,
                    reservation=InventoryReservation.objects.get(pk=reservation_id),
                )
                return "committed"
            except ValidationError:
                return "rejected"
            finally:
                close_old_connections()

        def release():
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                result = release_reservation(
                    organization=self.organization,
                    reservation=InventoryReservation.objects.get(pk=reservation_id),
                )
                return result.status
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            futures = [pool.submit(commit), pool.submit(release)]
            results = [f.result() for f in futures]
        reservation = InventoryReservation.objects.get(pk=reservation_id)
        self.batch.refresh_from_db()
        self.assertIn(reservation.status, {"committed", "released"})
        self.assertEqual(self.batch.quantity_reserved, Decimal("0"))
        self.assertIn(self.batch.quantity_available, {Decimal("6"), Decimal("10")})

    def test_concurrent_purchase_approval_has_single_winner(self):
        supplier = Supplier.objects.create(
            organization=self.organization, code="SUP-CONC", name="Concurrency Supplier"
        )
        order = PurchaseOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            supplier=supplier,
            order_number="PO-CONC-001",
        )
        requester = create_user(self.organization)
        approval = request_purchase_approval(
            organization=self.organization, purchase_order=order, actor_id=requester.id
        )
        approval_id = approval.id
        approver = create_user(self.organization)
        barrier = Barrier(2)

        def decide():
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                return decide_purchase_approval(
                    organization=self.organization,
                    approval=ProcurementApproval.objects.get(pk=approval_id),
                    approved=True,
                    actor_id=approver.id,
                )
            except ValidationError:
                return "rejected"
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: decide(), range(2)))
        self.assertEqual(sum(result != "rejected" for result in results), 1)
        approval.refresh_from_db()
        order.refresh_from_db()
        self.assertEqual(approval.status, "approved")
        self.assertEqual(order.status, "ordered")

    def test_concurrent_billing_creates_one_record(self):
        prescription = create_prescription(self.organization)
        prescription.medication = self.medication
        prescription.status = "active"
        prescription.quantity = Decimal("2")
        prescription.refills = 0
        prescription.start_date = timezone.localdate()
        prescription.end_date = timezone.localdate() + timedelta(days=2)
        prescription.save()
        order = DispensingOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            prescription=prescription,
            dispense_number="CONC-BILL-001",
            status="dispensed",
        )
        from apps.pharmacy.models import DispensingLine

        DispensingLine.objects.create(
            dispensing_order=order,
            product=self.product,
            batch=self.batch,
            quantity_prescribed=Decimal("2"),
            quantity_dispensed=Decimal("2"),
        )
        order_id = order.id
        barrier = Barrier(2)

        def bill():
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                return create_dispensing_bill(
                    organization=self.organization,
                    dispensing_order=DispensingOrder.objects.get(pk=order_id),
                )
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: bill(), range(2)))
        self.assertEqual(results[0][0].id, results[1][0].id)
        self.assertEqual(
            PharmacyBillingRecord.objects.filter(dispensing_order_id=order_id).count(),
            1,
        )

    def test_concurrent_idempotency_executes_callback_once(self):
        organization_id = self.organization.id
        calls = []

        def callback():
            calls.append("executed")
            return {"result": "stable"}, 201

        barrier = Barrier(2)

        def invoke():
            close_old_connections()
            try:
                barrier.wait(timeout=10)
                organization = apps.get_model(
                    "organizations", "Organization"
                ).objects.get(pk=organization_id)
                return execute_idempotent(
                    organization=organization,
                    key="conc-key",
                    operation="inventory.receive",
                    callback=callback,
                )
            finally:
                close_old_connections()

        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: invoke(), range(2)))
        self.assertEqual(calls.count("executed"), 1)
        self.assertEqual(results[0][0], {"result": "stable"})
        self.assertEqual(results[1][0], {"result": "stable"})
