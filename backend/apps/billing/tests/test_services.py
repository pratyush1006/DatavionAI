"""
Tests for billing services.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from apps.billing.constants import (
    ClaimStatus,
    InvoiceStatus,
    PaymentMethod,
)
from apps.billing.models import Invoice, Payment
from apps.billing.services import (
    InsuranceClaimService,
    InvoiceService,
    PaymentService,
    appeal_claim,
    approve_claim,
    reject_claim,
    settle_claim,
    update_invoice,
    void_invoice,
)
from apps.billing.tests.factories import (
    InsuranceClaimFactory,
    InvoiceFactory,
)
from apps.common.tests.base import BaseTestCase


class InvoiceServiceTestCase(BaseTestCase):
    """
    Test cases for InvoiceService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

    def test_create_invoice(self) -> None:
        """
        Invoice should be created successfully.
        """

        invoice = InvoiceService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "invoice_number": "INV000001",
                "invoice_date": date(
                    2025,
                    1,
                    1,
                ),
                "due_date": date(
                    2025,
                    1,
                    31,
                ),
                "total_amount": Decimal("1000.00"),
                "balance_amount": Decimal("1000.00"),
                "status": InvoiceStatus.DRAFT,
            },
        )

        self.assertIsInstance(
            invoice,
            Invoice,
        )

        self.assertEqual(
            invoice.organization,
            self.organization,
        )

        self.assertEqual(
            invoice.invoice_number,
            "INV000001",
        )

    def test_create_invoice_persists_to_database(self) -> None:
        """
        Created invoice should be persisted.
        """

        initial_count = Invoice.objects.count()

        InvoiceService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "invoice_number": "INV000002",
                "invoice_date": date(
                    2025,
                    1,
                    1,
                ),
                "due_date": date(
                    2025,
                    1,
                    31,
                ),
                "total_amount": Decimal("500.00"),
                "balance_amount": Decimal("500.00"),
                "status": InvoiceStatus.DRAFT,
            },
        )

        self.assertEqual(
            Invoice.objects.count(),
            initial_count + 1,
        )

    def test_update_invoice(self) -> None:
        """
        Invoice should be updated successfully.
        """

        invoice = InvoiceFactory(
            organization=self.organization,
            patient=self.patient,
        )

        updated_invoice = update_invoice(
            instance=invoice,
            validated_data={
                "notes": "Updated notes",
            },
        )

        updated_invoice.refresh_from_db()

        self.assertEqual(
            updated_invoice.notes,
            "Updated notes",
        )

    def test_void_invoice(self) -> None:
        """
        Invoice should be voided successfully.
        """

        invoice = InvoiceFactory(
            organization=self.organization,
            patient=self.patient,
            status=InvoiceStatus.DRAFT,
        )

        voided_invoice = void_invoice(
            instance=invoice,
        )

        voided_invoice.refresh_from_db()

        self.assertEqual(
            voided_invoice.status,
            InvoiceStatus.VOID,
        )

    def test_bulk_create_invoices(self) -> None:
        """
        Multiple invoices should be created successfully.
        """

        invoices = InvoiceService.bulk_create(
            validated_data_list=[
                {
                    "organization": self.organization,
                    "patient": self.patient,
                    "invoice_number": "INV000010",
                    "invoice_date": date(
                        2025,
                        1,
                        1,
                    ),
                    "due_date": date(
                        2025,
                        1,
                        31,
                    ),
                    "total_amount": Decimal("500.00"),
                    "balance_amount": Decimal("500.00"),
                    "status": InvoiceStatus.DRAFT,
                },
                {
                    "organization": self.organization,
                    "patient": self.patient,
                    "invoice_number": "INV000011",
                    "invoice_date": date(
                        2025,
                        1,
                        2,
                    ),
                    "due_date": date(
                        2025,
                        2,
                        28,
                    ),
                    "total_amount": Decimal("750.00"),
                    "balance_amount": Decimal("750.00"),
                    "status": InvoiceStatus.DRAFT,
                },
            ],
        )

        self.assertEqual(
            len(invoices),
            2,
        )


class PaymentServiceTestCase(BaseTestCase):
    """
    Test cases for PaymentService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

        self.invoice = InvoiceFactory(
            organization=self.organization,
            patient=self.patient,
            total_amount=Decimal("1000.00"),
            paid_amount=Decimal("0.00"),
            balance_amount=Decimal("1000.00"),
        )

    def test_create_payment(self) -> None:
        """
        Payment should be created successfully.
        """

        payment = PaymentService.create(
            validated_data={
                "organization": self.organization,
                "invoice": self.invoice,
                "patient": self.patient,
                "payment_method": PaymentMethod.CASH,
                "amount": Decimal("500.00"),
                "payment_date": date(
                    2025,
                    1,
                    15,
                ),
            },
        )

        self.assertIsInstance(
            payment,
            Payment,
        )

        self.assertEqual(
            payment.amount,
            Decimal("500.00"),
        )

    def test_create_payment_updates_invoice_balance(self) -> None:
        """
        Creating a payment should update the invoice balance.
        """

        PaymentService.create(
            validated_data={
                "organization": self.organization,
                "invoice": self.invoice,
                "patient": self.patient,
                "payment_method": PaymentMethod.CASH,
                "amount": Decimal("300.00"),
                "payment_date": date(
                    2025,
                    1,
                    15,
                ),
            },
        )

        self.invoice.refresh_from_db()

        self.assertEqual(
            self.invoice.paid_amount,
            Decimal("300.00"),
        )

        self.assertEqual(
            self.invoice.balance_amount,
            Decimal("700.00"),
        )

        self.assertEqual(
            self.invoice.status,
            InvoiceStatus.PARTIALLY_PAID,
        )

    def test_create_full_payment_marks_invoice_paid(self) -> None:
        """
        Full payment should mark the invoice as paid.
        """

        PaymentService.create(
            validated_data={
                "organization": self.organization,
                "invoice": self.invoice,
                "patient": self.patient,
                "payment_method": PaymentMethod.CARD,
                "amount": Decimal("1000.00"),
                "payment_date": date(
                    2025,
                    1,
                    15,
                ),
            },
        )

        self.invoice.refresh_from_db()

        self.assertEqual(
            self.invoice.status,
            InvoiceStatus.PAID,
        )

        self.assertEqual(
            self.invoice.balance_amount,
            Decimal("0.00"),
        )

    def test_bulk_create_payments(self) -> None:
        """
        Multiple payments should be created successfully.
        """

        payments = PaymentService.bulk_create(
            validated_data_list=[
                {
                    "organization": self.organization,
                    "invoice": self.invoice,
                    "patient": self.patient,
                    "payment_method": PaymentMethod.CASH,
                    "amount": Decimal("300.00"),
                    "payment_date": date(
                        2025,
                        1,
                        15,
                    ),
                },
                {
                    "organization": self.organization,
                    "invoice": self.invoice,
                    "patient": self.patient,
                    "payment_method": PaymentMethod.UPI,
                    "amount": Decimal("200.00"),
                    "payment_date": date(
                        2025,
                        1,
                        16,
                    ),
                },
            ],
        )

        self.assertEqual(
            len(payments),
            2,
        )

        self.invoice.refresh_from_db()

        self.assertEqual(
            self.invoice.paid_amount,
            Decimal("500.00"),
        )


class InsuranceClaimServiceTestCase(BaseTestCase):
    """
    Test cases for InsuranceClaimService.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

        self.invoice = InvoiceFactory(
            organization=self.organization,
            patient=self.patient,
        )

    def test_create_claim(self) -> None:
        """
        Insurance claim should be created successfully.
        """

        claim = InsuranceClaimService.create(
            validated_data={
                "organization": self.organization,
                "patient": self.patient,
                "invoice": self.invoice,
                "insurance_provider": "Test Insurance",
                "policy_number": "POL123456",
                "claim_number": "CLM000001",
                "claim_amount": Decimal("800.00"),
                "status": ClaimStatus.SUBMITTED,
            },
        )

        self.assertEqual(
            claim.insurance_provider,
            "Test Insurance",
        )

        self.assertEqual(
            claim.status,
            ClaimStatus.SUBMITTED,
        )

    def test_approve_claim(self) -> None:
        """
        Insurance claim should be approved successfully.
        """

        claim = InsuranceClaimFactory(
            organization=self.organization,
            patient=self.patient,
            invoice=self.invoice,
            claim_amount=Decimal("800.00"),
            status=ClaimStatus.SUBMITTED,
        )

        approved_claim = approve_claim(
            instance=claim,
            approved_amount=Decimal("800.00"),
        )

        approved_claim.refresh_from_db()

        self.assertEqual(
            approved_claim.status,
            ClaimStatus.APPROVED,
        )

        self.assertEqual(
            approved_claim.approved_amount,
            Decimal("800.00"),
        )

    def test_partially_approve_claim(self) -> None:
        """
        Insurance claim should be partially approved when amount is less.
        """

        claim = InsuranceClaimFactory(
            organization=self.organization,
            patient=self.patient,
            invoice=self.invoice,
            claim_amount=Decimal("1000.00"),
            status=ClaimStatus.SUBMITTED,
        )

        approved_claim = approve_claim(
            instance=claim,
            approved_amount=Decimal("600.00"),
        )

        approved_claim.refresh_from_db()

        self.assertEqual(
            approved_claim.status,
            ClaimStatus.PARTIALLY_APPROVED,
        )

        self.assertEqual(
            approved_claim.approved_amount,
            Decimal("600.00"),
        )

    def test_reject_claim(self) -> None:
        """
        Insurance claim should be rejected successfully.
        """

        claim = InsuranceClaimFactory(
            organization=self.organization,
            patient=self.patient,
            invoice=self.invoice,
            status=ClaimStatus.SUBMITTED,
        )

        rejected_claim = reject_claim(
            instance=claim,
            rejection_reason="Missing documentation",
        )

        rejected_claim.refresh_from_db()

        self.assertEqual(
            rejected_claim.status,
            ClaimStatus.REJECTED,
        )

        self.assertEqual(
            rejected_claim.rejection_reason,
            "Missing documentation",
        )

    def test_appeal_claim(self) -> None:
        """
        Rejected claim should be appealed successfully.
        """

        claim = InsuranceClaimFactory(
            organization=self.organization,
            patient=self.patient,
            invoice=self.invoice,
            status=ClaimStatus.REJECTED,
        )

        appealed_claim = appeal_claim(
            instance=claim,
        )

        appealed_claim.refresh_from_db()

        self.assertEqual(
            appealed_claim.status,
            ClaimStatus.APPEALED,
        )

    def test_settle_claim(self) -> None:
        """
        Approved claim should be settled successfully.
        """

        claim = InsuranceClaimFactory(
            organization=self.organization,
            patient=self.patient,
            invoice=self.invoice,
            claim_amount=Decimal("800.00"),
            approved_amount=Decimal("800.00"),
            status=ClaimStatus.APPROVED,
        )

        settled_claim = settle_claim(
            instance=claim,
        )

        settled_claim.refresh_from_db()

        self.assertEqual(
            settled_claim.status,
            ClaimStatus.SETTLED,
        )

        self.assertIsNotNone(
            settled_claim.settled_at,
        )

    def test_bulk_create_claims(self) -> None:
        """
        Multiple claims should be created successfully.
        """

        claims = InsuranceClaimService.bulk_create(
            validated_data_list=[
                {
                    "organization": self.organization,
                    "patient": self.patient,
                    "invoice": self.invoice,
                    "insurance_provider": "Test Insurance",
                    "policy_number": "POL123456",
                    "claim_number": "CLM000010",
                    "claim_amount": Decimal("500.00"),
                    "status": ClaimStatus.SUBMITTED,
                },
                {
                    "organization": self.organization,
                    "patient": self.patient,
                    "invoice": self.invoice,
                    "insurance_provider": "Test Insurance",
                    "policy_number": "POL123456",
                    "claim_number": "CLM000011",
                    "claim_amount": Decimal("700.00"),
                    "status": ClaimStatus.SUBMITTED,
                },
            ],
        )

        self.assertEqual(
            len(claims),
            2,
        )


__all__ = [
    "InsuranceClaimServiceTestCase",
    "InvoiceServiceTestCase",
    "PaymentServiceTestCase",
]
