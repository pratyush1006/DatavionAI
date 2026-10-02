from datetime import timedelta
from decimal import Decimal
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.pharmacy.models import (
    InventoryReservation,
    MedicationBatch,
    Pharmacy,
    PharmacyProduct,
)
from apps.pharmacy.services.audit import record_audit
from apps.pharmacy.services.inventory import receive_stock
from apps.pharmacy.services.reservations import (
    commit_reservation,
    release_reservation,
    reserve_stock,
)
from apps.pharmacy.tests.factories import create_medication, create_organization


class PharmacyProductionControlTests(TestCase):
    def setUp(self):
        self.organization = create_organization("Production Controls Org")
        self.pharmacy = Pharmacy.objects.create(
            organization=self.organization, code="MAIN", name="Main Pharmacy"
        )
        self.medication = create_medication(self.organization)
        self.product = PharmacyProduct.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            medication=self.medication,
            sku="PROD-CTRL",
            selling_price=Decimal("10.00"),
        )
        self.batch = MedicationBatch.objects.create(
            product=self.product,
            batch_number="PC-001",
            expiry_date=timezone.localdate() + timedelta(days=180),
        )
        receive_stock(organization=self.organization, batch=self.batch, quantity=20)

    def test_reservation_reduces_available_capacity(self):
        reservation = reserve_stock(
            organization=self.organization,
            batch=self.batch,
            quantity=7,
            reservation_number="RES-PC-001",
        )
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_reserved, Decimal("7"))
        self.assertEqual(
            self.batch.quantity_available - self.batch.quantity_reserved, Decimal("13")
        )
        self.assertEqual(reservation.status, "active")

    def test_release_reservation_restores_capacity(self):
        reservation = reserve_stock(
            organization=self.organization,
            batch=self.batch,
            quantity=5,
            reservation_number="RES-PC-002",
        )
        release_reservation(organization=self.organization, reservation=reservation)
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_reserved, Decimal("0"))
        reservation.refresh_from_db()
        self.assertEqual(reservation.status, "released")

    def test_commit_reservation_consumes_stock(self):
        reservation = reserve_stock(
            organization=self.organization,
            batch=self.batch,
            quantity=6,
            reservation_number="RES-PC-003",
        )
        commit_reservation(organization=self.organization, reservation=reservation)
        self.batch.refresh_from_db()
        reservation.refresh_from_db()
        self.assertEqual(self.batch.quantity_available, Decimal("14"))
        self.assertEqual(self.batch.quantity_reserved, Decimal("0"))
        self.assertEqual(reservation.status, "committed")

    def test_expired_reservation_cannot_commit(self):
        reservation = reserve_stock(
            organization=self.organization,
            batch=self.batch,
            quantity=2,
            reservation_number="RES-PC-004",
            expires_at=timezone.now() - timedelta(minutes=1),
        )
        with self.assertRaisesMessage(ValidationError, "expired"):
            commit_reservation(organization=self.organization, reservation=reservation)
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_reserved, Decimal("0"))

    def test_audit_record_is_organization_scoped(self):
        log = record_audit(
            organization=self.organization,
            action="stock.received",
            entity_type="MedicationBatch",
            entity_id=self.batch.id,
            payload={"quantity": "20"},
        )
        self.assertEqual(log.organization_id, self.organization.id)
        self.assertEqual(log.entity_id, self.batch.id)
        self.assertEqual(
            InventoryReservation.objects.filter(organization=self.organization).count(),
            0,
        )

    def _create_active_prescription(self, quantity=10, refills=0):
        from apps.pharmacy.tests.factories import create_prescription

        prescription = create_prescription(self.organization)
        prescription.medication = self.medication
        prescription.quantity = Decimal(str(quantity))
        prescription.refills = refills
        prescription.status = "active"
        prescription.start_date = timezone.localdate()
        prescription.end_date = timezone.localdate() + timedelta(days=30)
        prescription.save(
            update_fields=[
                "medication",
                "quantity",
                "refills",
                "status",
                "start_date",
                "end_date",
                "updated_at",
            ]
        )
        return prescription

    def test_dispensing_requires_active_matching_prescription(self):
        from apps.pharmacy.models import DispensingOrder
        from apps.pharmacy.services.dispensing import dispense_order

        prescription = self._create_active_prescription(quantity=5, refills=0)
        order = DispensingOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            prescription=prescription,
            dispense_number="RX-DISP-001",
        )
        with self.assertRaisesMessage(ValidationError, "pharmacist actor"):
            dispense_order(
                organization=self.organization,
                order=order,
                requested_lines=[{"product": self.product, "quantity": Decimal("1")}],
            )

    def test_dispensing_rejects_wrong_medication(self):
        from apps.pharmacy.models import DispensingOrder
        from apps.pharmacy.services.dispensing import dispense_order

        prescription = self._create_active_prescription(quantity=5, refills=0)
        other_medication = create_medication(self.organization)
        other_product = PharmacyProduct.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            medication=other_medication,
            sku="WRONG-MED",
            selling_price=Decimal("10.00"),
        )
        order = DispensingOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            prescription=prescription,
            dispense_number="RX-DISP-002",
        )
        with self.assertRaisesMessage(
            ValidationError, "does not match the prescription"
        ):
            dispense_order(
                organization=self.organization,
                order=order,
                pharmacist_id=uuid4(),
                requested_lines=[{"product": other_product, "quantity": Decimal("1")}],
            )

    def test_dispensing_cannot_exceed_prescription_allowance(self):
        from apps.pharmacy.models import DispensingOrder
        from apps.pharmacy.services.dispensing import dispense_order

        prescription = self._create_active_prescription(quantity=5, refills=0)
        order = DispensingOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            prescription=prescription,
            dispense_number="RX-DISP-003",
        )
        with self.assertRaisesMessage(
            ValidationError, "exceeds prescription allowance"
        ):
            dispense_order(
                organization=self.organization,
                order=order,
                pharmacist_id=uuid4(),
                requested_lines=[{"product": self.product, "quantity": Decimal("6")}],
            )

    def test_dispensing_allows_configured_refill_quantity(self):
        from apps.pharmacy.models import DispensingOrder
        from apps.pharmacy.services.dispensing import dispense_order

        prescription = self._create_active_prescription(quantity=5, refills=1)
        first = DispensingOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            prescription=prescription,
            dispense_number="RX-DISP-REFILL-001",
        )
        dispense_order(
            organization=self.organization,
            order=first,
            pharmacist_id=uuid4(),
            requested_lines=[{"product": self.product, "quantity": Decimal("5")}],
        )
        second = DispensingOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            prescription=prescription,
            dispense_number="RX-DISP-REFILL-002",
        )
        dispense_order(
            organization=self.organization,
            order=second,
            pharmacist_id=uuid4(),
            requested_lines=[{"product": self.product, "quantity": Decimal("5")}],
        )
        self.assertEqual(second.status, "dispensed")

    def test_dispensing_rejects_quantity_beyond_refill_allowance(self):
        from apps.pharmacy.models import DispensingOrder
        from apps.pharmacy.services.dispensing import dispense_order

        prescription = self._create_active_prescription(quantity=5, refills=1)
        first = DispensingOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            prescription=prescription,
            dispense_number="RX-DISP-REFILL-003",
        )
        dispense_order(
            organization=self.organization,
            order=first,
            pharmacist_id=uuid4(),
            requested_lines=[{"product": self.product, "quantity": Decimal("5")}],
        )
        second = DispensingOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            prescription=prescription,
            dispense_number="RX-DISP-REFILL-004",
        )
        with self.assertRaisesMessage(
            ValidationError, "exceeds prescription allowance"
        ):
            dispense_order(
                organization=self.organization,
                order=second,
                pharmacist_id=uuid4(),
                requested_lines=[{"product": self.product, "quantity": Decimal("6")}],
            )

    def test_dispensing_preserves_patient_linkage_through_prescription(self):
        from apps.pharmacy.models import DispensingOrder

        prescription = self._create_active_prescription(quantity=5, refills=1)
        order = DispensingOrder.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            prescription=prescription,
            dispense_number="RX-DISP-004",
        )
        self.assertEqual(order.prescription.patient_id, prescription.patient_id)
