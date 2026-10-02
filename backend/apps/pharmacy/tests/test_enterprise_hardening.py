from datetime import timedelta
from decimal import Decimal

from django.apps import apps
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.pharmacy.models import (
    ControlledSubstanceControl,
    MedicationBatch,
    PharmacyBillingRecord,
    PharmacyProduct,
    PurchaseOrder,
    Supplier,
)
from apps.pharmacy.services.billing import create_dispensing_bill
from apps.pharmacy.services.compliance import (
    initiate_recall,
    quarantine_batch,
    release_quarantine,
    validate_controlled_dispensing,
)
from apps.pharmacy.services.procurement import (
    decide_purchase_approval,
    request_purchase_approval,
)
from apps.pharmacy.tests.factories import (
    create_medication,
    create_organization,
    create_pharmacy,
    create_user,
)


class PharmacyEnterpriseHardeningTests(TestCase):
    def setUp(self):
        self.organization = create_organization()
        self.pharmacy = create_pharmacy(self.organization)
        self.medication = create_medication(self.organization)
        self.product = PharmacyProduct.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            medication=self.medication,
            sku="SKU-HARDEN-001",
            selling_price=Decimal("10.00"),
            tax_rate=Decimal("5.000"),
        )
        self.batch = MedicationBatch.objects.create(
            product=self.product,
            batch_number="B-HARDEN-001",
            expiry_date=timezone.localdate() + timedelta(days=180),
            quantity_received=Decimal("20"),
            quantity_available=Decimal("20"),
        )
        self.user = create_user(self.organization)

    def test_controlled_substance_requires_second_checker(self):
        ControlledSubstanceControl.objects.create(
            organization=self.organization,
            product=self.product,
            schedule="schedule_ii",
            requires_double_check=True,
        )
        with self.assertRaises(ValidationError):
            validate_controlled_dispensing(
                organization=self.organization, product=self.product, quantity=1
            )
        validate_controlled_dispensing(
            organization=self.organization,
            product=self.product,
            quantity=1,
            second_checker_id=self.user.id,
        )

    def test_quarantine_removes_and_release_restores_available_stock(self):
        q = quarantine_batch(
            organization=self.organization,
            batch=self.batch,
            quantity=Decimal("5"),
            reason="Quality hold",
            actor_id=self.user.id,
        )
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_available, Decimal("15"))
        release_quarantine(
            organization=self.organization, quarantine=q, actor_id=self.user.id
        )
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_available, Decimal("20"))

    def test_recall_reduces_available_stock_and_records_batch(self):
        recall = initiate_recall(
            organization=self.organization,
            product=self.product,
            recall_number="REC-001",
            reason="Manufacturer recall",
            batch_quantities=[{"batch": self.batch, "quantity": Decimal("4")}],
            actor_id=self.user.id,
        )
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_available, Decimal("16"))
        self.assertEqual(recall.batches.count(), 1)

    def test_procurement_approval_promotes_order_to_ordered(self):
        supplier = Supplier.objects.create(
            organization=self.organization, code="SUP-H1", name="Hardening Supplier"
        )
        order = PurchaseOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            supplier=supplier,
            order_number="PO-HARD-001",
        )
        approval = request_purchase_approval(
            organization=self.organization, purchase_order=order, actor_id=self.user.id
        )
        self.assertEqual(approval.status, "pending")
        approver = create_user(self.organization)
        if hasattr(approver, "username"):
            approver.username = f"pharmacy-approver-{approver.id}"
            approver.save(update_fields=["username"])
        decide_purchase_approval(
            organization=self.organization,
            approval=approval,
            approved=True,
            actor_id=approver.id,
        )
        order.refresh_from_db()
        self.assertEqual(order.status, "ordered")

    def test_billing_record_is_idempotent(self):
        DispensingOrder = apps.get_model("pharmacy", "DispensingOrder")
        DispensingLine = apps.get_model("pharmacy", "DispensingLine")
        from apps.pharmacy.tests.factories import create_prescription

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
            dispense_number="DISP-HARD-001",
            status="dispensed",
        )
        DispensingLine.objects.create(
            dispensing_order=order,
            product=self.product,
            batch=self.batch,
            quantity_prescribed=Decimal("2"),
            quantity_dispensed=Decimal("2"),
        )
        first, created1 = create_dispensing_bill(
            organization=self.organization, dispensing_order=order
        )
        second, created2 = create_dispensing_bill(
            organization=self.organization, dispensing_order=order
        )
        self.assertTrue(created1)
        self.assertFalse(created2)
        self.assertEqual(first.id, second.id)
        self.assertEqual(
            PharmacyBillingRecord.objects.filter(dispensing_order=order).count(), 1
        )
