"""
Tests for the Billing models.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from django.db import IntegrityError

from apps.billing.constants import (
    DEFAULT_INVOICE_STATUS,
    ClaimStatus,
    InvoiceStatus,
    PaymentMethod,
)
from apps.billing.models import (
    InsuranceClaim,
    Invoice,
    InvoiceItem,
    Payment,
)
from apps.common.tests.base import BaseTestCase


class InvoiceModelTestCase(BaseTestCase):
    """
    Test cases for the Invoice model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

        self.invoice = Invoice.objects.create(
            organization=self.organization,
            patient=self.patient,
            invoice_number="INV000001",
            invoice_date=date(
                2025,
                1,
                1,
            ),
            due_date=date(
                2025,
                1,
                31,
            ),
            total_amount=Decimal("1000.00"),
            paid_amount=Decimal("0.00"),
            balance_amount=Decimal("1000.00"),
            status=DEFAULT_INVOICE_STATUS,
        )

    def test_invoice_creation(self) -> None:
        """
        Invoice should be created successfully.
        """

        self.assertEqual(
            self.invoice.organization,
            self.organization,
        )

        self.assertEqual(
            self.invoice.patient,
            self.patient,
        )

        self.assertEqual(
            self.invoice.invoice_number,
            "INV000001",
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the invoice display string.
        """

        self.assertIn(
            "INV000001",
            str(self.invoice),
        )

    def test_default_status(self) -> None:
        """
        Default invoice status should be applied.
        """

        self.assertEqual(
            self.invoice.status,
            DEFAULT_INVOICE_STATUS,
        )

    def test_is_paid_property(self) -> None:
        """
        is_paid should return True when status is PAID.
        """

        self.assertFalse(
            self.invoice.is_paid,
        )

        self.invoice.status = InvoiceStatus.PAID

        self.assertTrue(
            self.invoice.is_paid,
        )

    def test_meta_table_name(self) -> None:
        """
        Invoice model should use the configured database table.
        """

        self.assertEqual(
            Invoice._meta.db_table,
            "invoices",
        )

    def test_unique_invoice_number(self) -> None:
        """
        Invoice number should be unique.
        """

        with self.assertRaises(
            IntegrityError,
        ):
            Invoice.objects.create(
                organization=self.organization,
                patient=self.patient,
                invoice_number="INV000001",
                invoice_date=date(
                    2025,
                    2,
                    1,
                ),
                due_date=date(
                    2025,
                    2,
                    28,
                ),
                total_amount=Decimal("500.00"),
                paid_amount=Decimal("0.00"),
                balance_amount=Decimal("500.00"),
            )

    def test_foreign_key_relationships(self) -> None:
        """
        Invoice should have proper foreign key relationships.
        """

        self.assertEqual(
            self.invoice.organization,
            self.organization,
        )

        self.assertEqual(
            self.invoice.patient,
            self.patient,
        )


class InvoiceItemModelTestCase(BaseTestCase):
    """
    Test cases for the InvoiceItem model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

        self.invoice = Invoice.objects.create(
            organization=self.organization,
            patient=self.patient,
            invoice_number="INV000002",
            invoice_date=date(
                2025,
                1,
                1,
            ),
            due_date=date(
                2025,
                1,
                31,
            ),
            total_amount=Decimal("1000.00"),
            paid_amount=Decimal("0.00"),
            balance_amount=Decimal("1000.00"),
        )

        self.invoice_item = InvoiceItem.objects.create(
            invoice=self.invoice,
            description="Consultation Fee",
            quantity=2,
            unit_price=Decimal("250.00"),
            total_price=Decimal("500.00"),
            service_code="CPT-99213",
        )

    def test_invoice_item_creation(self) -> None:
        """
        InvoiceItem should be created successfully.
        """

        self.assertEqual(
            self.invoice_item.invoice,
            self.invoice,
        )

        self.assertEqual(
            self.invoice_item.description,
            "Consultation Fee",
        )

        self.assertEqual(
            self.invoice_item.quantity,
            2,
        )

    def test_save_calculates_total_price(self) -> None:
        """
        save() should calculate total_price from quantity and unit_price.
        """

        self.invoice_item.quantity = 3
        self.invoice_item.unit_price = Decimal("100.00")
        self.invoice_item.save()

        self.invoice_item.refresh_from_db()

        self.assertEqual(
            self.invoice_item.total_price,
            Decimal("300.00"),
        )

    def test_meta_table_name(self) -> None:
        """
        InvoiceItem model should use the configured database table.
        """

        self.assertEqual(
            InvoiceItem._meta.db_table,
            "invoice_items",
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the invoice item display string.
        """

        self.assertIn(
            "Consultation Fee",
            str(self.invoice_item),
        )


class PaymentModelTestCase(BaseTestCase):
    """
    Test cases for the Payment model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

        self.invoice = Invoice.objects.create(
            organization=self.organization,
            patient=self.patient,
            invoice_number="INV000003",
            invoice_date=date(
                2025,
                1,
                1,
            ),
            due_date=date(
                2025,
                1,
                31,
            ),
            total_amount=Decimal("1000.00"),
            paid_amount=Decimal("0.00"),
            balance_amount=Decimal("1000.00"),
        )

        self.payment = Payment.objects.create(
            organization=self.organization,
            invoice=self.invoice,
            patient=self.patient,
            payment_method=PaymentMethod.CASH,
            amount=Decimal("500.00"),
            payment_date=date(
                2025,
                1,
                15,
            ),
        )

    def test_payment_creation(self) -> None:
        """
        Payment should be created successfully.
        """

        self.assertEqual(
            self.payment.organization,
            self.organization,
        )

        self.assertEqual(
            self.payment.invoice,
            self.invoice,
        )

        self.assertEqual(
            self.payment.payment_method,
            PaymentMethod.CASH,
        )

        self.assertEqual(
            self.payment.amount,
            Decimal("500.00"),
        )

    def test_meta_table_name(self) -> None:
        """
        Payment model should use the configured database table.
        """

        self.assertEqual(
            Payment._meta.db_table,
            "payments",
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the payment display string.
        """

        self.assertIn(
            "cash",
            str(self.payment),
        )

    def test_foreign_key_relationships(self) -> None:
        """
        Payment should have proper foreign key relationships.
        """

        self.assertEqual(
            self.payment.organization,
            self.organization,
        )

        self.assertEqual(
            self.payment.patient,
            self.patient,
        )

        self.assertEqual(
            self.payment.invoice,
            self.invoice,
        )


class InsuranceClaimModelTestCase(BaseTestCase):
    """
    Test cases for the InsuranceClaim model.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

        self.invoice = Invoice.objects.create(
            organization=self.organization,
            patient=self.patient,
            invoice_number="INV000004",
            invoice_date=date(
                2025,
                1,
                1,
            ),
            due_date=date(
                2025,
                1,
                31,
            ),
            total_amount=Decimal("1000.00"),
            paid_amount=Decimal("0.00"),
            balance_amount=Decimal("1000.00"),
        )

        self.claim = InsuranceClaim.objects.create(
            organization=self.organization,
            patient=self.patient,
            invoice=self.invoice,
            insurance_provider="Test Insurance Co.",
            policy_number="POL123456",
            claim_number="CLM000001",
            claim_amount=Decimal("800.00"),
            status=ClaimStatus.SUBMITTED,
        )

    def test_claim_creation(self) -> None:
        """
        InsuranceClaim should be created successfully.
        """

        self.assertEqual(
            self.claim.organization,
            self.organization,
        )

        self.assertEqual(
            self.claim.insurance_provider,
            "Test Insurance Co.",
        )

        self.assertEqual(
            self.claim.claim_number,
            "CLM000001",
        )

    def test_meta_table_name(self) -> None:
        """
        InsuranceClaim model should use the configured database table.
        """

        self.assertEqual(
            InsuranceClaim._meta.db_table,
            "billing_insurance_claims",
        )

    def test_string_representation(self) -> None:
        """
        __str__ should return the claim display string.
        """

        self.assertIn(
            "CLM000001",
            str(self.claim),
        )

    def test_unique_claim_number(self) -> None:
        """
        Claim number should be unique.
        """

        with self.assertRaises(
            IntegrityError,
        ):
            InsuranceClaim.objects.create(
                organization=self.organization,
                patient=self.patient,
                invoice=self.invoice,
                insurance_provider="Another Insurance",
                policy_number="POL999999",
                claim_number="CLM000001",
                claim_amount=Decimal("600.00"),
            )


__all__ = [
    "InsuranceClaimModelTestCase",
    "InvoiceItemModelTestCase",
    "InvoiceModelTestCase",
    "PaymentModelTestCase",
]
