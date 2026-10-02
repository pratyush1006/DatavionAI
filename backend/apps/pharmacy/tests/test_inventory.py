from datetime import timedelta
from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.pharmacy.models import MedicationBatch, Pharmacy, PharmacyProduct
from apps.pharmacy.services.inventory import dispense_stock, receive_stock, return_stock
from apps.pharmacy.tests.factories import create_medication, create_organization


class PharmacyInventoryTests(TestCase):
    def setUp(self):
        self.organization = create_organization()
        self.pharmacy = Pharmacy.objects.create(
            organization=self.organization, code="MAIN", name="Main Pharmacy"
        )
        self.medication = create_medication(self.organization)
        self.product = PharmacyProduct.objects.create(
            organization=self.organization,
            pharmacy=self.pharmacy,
            medication=self.medication,
            sku="AMOX-500",
            selling_price=Decimal("10.00"),
        )
        self.batch = MedicationBatch.objects.create(
            product=self.product,
            batch_number="B001",
            expiry_date=timezone.localdate() + timedelta(days=180),
        )

    def test_receive_increases_stock(self):
        receive_stock(organization=self.organization, batch=self.batch, quantity=100)
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_available, Decimal("100"))

    def test_expired_stock_is_blocked(self):
        self.batch.expiry_date = timezone.localdate() - timedelta(days=1)
        self.batch.quantity_available = 50
        self.batch.save(update_fields=["expiry_date", "quantity_available"])
        with self.assertRaisesMessage(ValidationError, "Expired medication"):
            dispense_stock(organization=self.organization, batch=self.batch, quantity=1)

    def test_negative_stock_is_blocked(self):
        with self.assertRaisesMessage(ValidationError, "Insufficient"):
            dispense_stock(organization=self.organization, batch=self.batch, quantity=1)

    def test_fefo_dispensing_uses_earliest_expiry_first(self):
        from apps.pharmacy.models import MedicationBatch
        from apps.pharmacy.services.inventory import dispense_product

        early = MedicationBatch.objects.create(
            product=self.product,
            batch_number="B000",
            expiry_date=timezone.localdate() + timedelta(days=30),
        )
        receive_stock(organization=self.organization, batch=early, quantity=5)
        receive_stock(organization=self.organization, batch=self.batch, quantity=20)
        movements = dispense_product(
            organization=self.organization, product=self.product, quantity=7
        )
        self.assertEqual(movements[0].batch_id, early.id)
        early.refresh_from_db()
        self.assertEqual(early.quantity_available, Decimal("0"))
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_available, Decimal("18"))

    def test_dispensing_reduces_stock(self):
        receive_stock(organization=self.organization, batch=self.batch, quantity=20)
        dispense_stock(organization=self.organization, batch=self.batch, quantity=7)
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_available, Decimal("13"))

    def test_restockable_return_increases_stock(self):
        receive_stock(organization=self.organization, batch=self.batch, quantity=20)
        return_stock(
            organization=self.organization,
            batch=self.batch,
            quantity=5,
            restockable=True,
        )
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_available, Decimal("25"))

    def test_non_restockable_return_preserves_stock(self):
        receive_stock(organization=self.organization, batch=self.batch, quantity=20)
        return_stock(
            organization=self.organization,
            batch=self.batch,
            quantity=5,
            restockable=False,
        )
        self.batch.refresh_from_db()
        self.assertEqual(self.batch.quantity_available, Decimal("20"))
