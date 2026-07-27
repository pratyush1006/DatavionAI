"""
Tests for the Accounts Receivable models.
"""

from __future__ import annotations

from apps.billing.accounts_receivable.models import (
    Customer,
    CustomerInvoice,
)
from apps.common.tests.base import BaseTestCase


class CustomerModelTestCase(BaseTestCase):
    """
    Test cases for the Customer model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.instance = Customer.objects.create(
            organization=self.organization,
            code="C001",
            name="Globex Corp",
        )

    def test_customer_creation(
        self,
    ) -> None:
        """
        Customer should be created successfully.
        """

        self.assertEqual(
            self.instance.organization,
            self.organization,
        )

        self.assertEqual(
            self.instance.name,
            "Globex Corp",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the customer display string.
        """

        self.assertIn(
            "Globex Corp",
            str(self.instance),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        Customer model should use the configured database table.
        """

        self.assertEqual(
            Customer._meta.db_table,
            "accounts_receivable_customers",
        )


class CustomerInvoiceModelTestCase(BaseTestCase):
    """
    Test cases for the CustomerInvoice model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()
        self.customer = Customer.objects.create(
            organization=self.organization,
            code="C001",
            name="Globex Corp",
        )

        self.instance = CustomerInvoice.objects.create(
            organization=self.organization,
            invoice_number="CINV-001",
            customer=self.customer,
        )

    def test_customer_invoice_creation(
        self,
    ) -> None:
        """
        CustomerInvoice should be created successfully.
        """

        self.assertEqual(
            self.instance.organization,
            self.organization,
        )

        self.assertEqual(
            self.instance.invoice_number,
            "CINV-001",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the customer_invoice display string.
        """

        self.assertIn(
            "CINV-001",
            str(self.instance),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        CustomerInvoice model should use the configured database table.
        """

        self.assertEqual(
            CustomerInvoice._meta.db_table,
            "accounts_receivable_customer_invoices",
        )


__all__ = [
    "CustomerModelTestCase",
    "CustomerInvoiceModelTestCase",
]
