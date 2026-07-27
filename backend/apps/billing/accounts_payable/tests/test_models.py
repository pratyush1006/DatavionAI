"""
Tests for the Accounts Payable models.
"""

from __future__ import annotations

from apps.billing.accounts_payable.models import (
    Vendor,
    VendorInvoice,
)
from apps.common.tests.base import BaseTestCase


class VendorModelTestCase(BaseTestCase):
    """
    Test cases for the Vendor model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.instance = Vendor.objects.create(
            organization=self.organization,
            code="V001",
            name="Acme Supplies",
        )

    def test_vendor_creation(
        self,
    ) -> None:
        """
        Vendor should be created successfully.
        """

        self.assertEqual(
            self.instance.organization,
            self.organization,
        )

        self.assertEqual(
            self.instance.name,
            "Acme Supplies",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the vendor display string.
        """

        self.assertIn(
            "Acme Supplies",
            str(self.instance),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        Vendor model should use the configured database table.
        """

        self.assertEqual(
            Vendor._meta.db_table,
            "accounts_payable_vendors",
        )


class VendorInvoiceModelTestCase(BaseTestCase):
    """
    Test cases for the VendorInvoice model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()
        self.vendor = Vendor.objects.create(
            organization=self.organization,
            code="V001",
            name="Acme Supplies",
        )

        self.instance = VendorInvoice.objects.create(
            organization=self.organization,
            invoice_number="INV-001",
            vendor=self.vendor,
        )

    def test_vendor_invoice_creation(
        self,
    ) -> None:
        """
        VendorInvoice should be created successfully.
        """

        self.assertEqual(
            self.instance.organization,
            self.organization,
        )

        self.assertEqual(
            self.instance.invoice_number,
            "INV-001",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the vendor_invoice display string.
        """

        self.assertIn(
            "INV-001",
            str(self.instance),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        VendorInvoice model should use the configured database table.
        """

        self.assertEqual(
            VendorInvoice._meta.db_table,
            "accounts_payable_vendor_invoices",
        )


__all__ = [
    "VendorModelTestCase",
    "VendorInvoiceModelTestCase",
]
