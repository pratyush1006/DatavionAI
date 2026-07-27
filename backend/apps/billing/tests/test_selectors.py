"""
Tests for billing selectors.
"""

from __future__ import annotations

from datetime import date
from decimal import Decimal

from apps.billing.constants import (
    InvoiceStatus,
    PaymentMethod,
)
from apps.billing.selectors import (
    InvoiceSelector,
    PaymentSelector,
)
from apps.billing.tests.factories import (
    InvoiceFactory,
    PaymentFactory,
)
from apps.common.tests.base import BaseTestCase


class InvoiceSelectorTestCase(BaseTestCase):
    """
    Test cases for InvoiceSelector.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

        self.active_invoice = InvoiceFactory(
            organization=self.organization,
            patient=self.patient,
            invoice_number="INV000001",
            status=InvoiceStatus.DRAFT,
            total_amount=Decimal("1000.00"),
            paid_amount=Decimal("0.00"),
            balance_amount=Decimal("1000.00"),
        )

        self.overdue_invoice = InvoiceFactory(
            organization=self.organization,
            patient=self.patient,
            invoice_number="INV000002",
            status=InvoiceStatus.OVERDUE,
            invoice_date=date(
                2024,
                1,
                1,
            ),
            due_date=date(
                2024,
                1,
                31,
            ),
            total_amount=Decimal("500.00"),
            paid_amount=Decimal("0.00"),
            balance_amount=Decimal("500.00"),
        )

    def test_queryset(self) -> None:
        """
        queryset() should return a queryset.
        """

        queryset = InvoiceSelector.queryset()

        self.assertIn(
            self.active_invoice,
            queryset,
        )

    def test_get(self) -> None:
        """
        get() should return the requested invoice.
        """

        invoice = InvoiceSelector.get(
            invoice_id=self.active_invoice.id,
        )

        self.assertEqual(
            invoice,
            self.active_invoice,
        )

    def test_list(self) -> None:
        """
        list() should return all invoices.
        """

        invoices = InvoiceSelector.list()

        self.assertEqual(
            invoices.count(),
            2,
        )

    def test_list_by_patient(self) -> None:
        """
        list_by_patient() should filter by patient.
        """

        invoices = InvoiceSelector.list_by_patient(
            patient_id=self.patient.id,
        )

        self.assertEqual(
            invoices.count(),
            2,
        )

    def test_list_by_organization(self) -> None:
        """
        list_by_organization() should filter by organization.
        """

        invoices = InvoiceSelector.list_by_organization(
            organization=self.organization,
        )

        self.assertEqual(
            invoices.count(),
            2,
        )

    def test_search(self) -> None:
        """
        search() should find matching invoices.
        """

        invoices = InvoiceSelector.search(
            organization=self.organization,
            query="INV000001",
        )

        self.assertEqual(
            invoices.count(),
            1,
        )

        self.assertEqual(
            invoices.first(),
            self.active_invoice,
        )

    def test_count(self) -> None:
        """
        count() should return the invoice count.
        """

        self.assertEqual(
            InvoiceSelector.count(
                organization=self.organization,
            ),
            2,
        )

    def test_list_overdue(self) -> None:
        """
        list_overdue() should return overdue invoices.
        """

        invoices = InvoiceSelector.list_overdue(
            organization=self.organization,
        )

        self.assertIn(
            self.overdue_invoice,
            invoices,
        )


class PaymentSelectorTestCase(BaseTestCase):
    """
    Test cases for PaymentSelector.
    """

    def setUp(self) -> None:
        super().setUp()

        self.patient = self.create_patient()

        self.invoice = InvoiceFactory(
            organization=self.organization,
            patient=self.patient,
        )

        self.payment = PaymentFactory(
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

    def test_queryset(self) -> None:
        """
        queryset() should return a queryset.
        """

        queryset = PaymentSelector.queryset()

        self.assertIn(
            self.payment,
            queryset,
        )

    def test_get(self) -> None:
        """
        get() should return the requested payment.
        """

        payment = PaymentSelector.get(
            payment_id=self.payment.id,
        )

        self.assertEqual(
            payment,
            self.payment,
        )

    def test_list(self) -> None:
        """
        list() should return all payments.
        """

        payments = PaymentSelector.list()

        self.assertEqual(
            payments.count(),
            1,
        )

    def test_list_by_invoice(self) -> None:
        """
        list_by_invoice() should filter by invoice.
        """

        payments = PaymentSelector.list_by_invoice(
            invoice_id=self.invoice.id,
        )

        self.assertEqual(
            payments.count(),
            1,
        )

    def test_list_by_patient(self) -> None:
        """
        list_by_patient() should filter by patient.
        """

        payments = PaymentSelector.list_by_patient(
            patient_id=self.patient.id,
        )

        self.assertEqual(
            payments.count(),
            1,
        )

    def test_list_by_organization(self) -> None:
        """
        list_by_organization() should filter by organization.
        """

        payments = PaymentSelector.list_by_organization(
            organization=self.organization,
        )

        self.assertEqual(
            payments.count(),
            1,
        )

    def test_list_by_date_range(self) -> None:
        """
        list_by_date_range() should filter by date range.
        """

        payments = PaymentSelector.list_by_date_range(
            organization=self.organization,
            start_date=date(
                2025,
                1,
                1,
            ),
            end_date=date(
                2025,
                1,
                31,
            ),
        )

        self.assertEqual(
            payments.count(),
            1,
        )


__all__ = [
    "InvoiceSelectorTestCase",
    "PaymentSelectorTestCase",
]
