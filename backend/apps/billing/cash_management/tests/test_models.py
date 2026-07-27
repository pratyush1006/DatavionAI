"""
Tests for the Cash Management models.
"""

from __future__ import annotations

from apps.billing.cash_management.models import (
    BankAccount,
    CashTransaction,
)
from apps.common.tests.base import BaseTestCase


class BankAccountModelTestCase(BaseTestCase):
    """
    Test cases for the BankAccount model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.instance = BankAccount.objects.create(
            organization=self.organization,
            name="HDFC",
            account_number="ACC001",
            bank_name="HDFC Bank",
        )

    def test_bank_account_creation(
        self,
    ) -> None:
        """
        BankAccount should be created successfully.
        """

        self.assertEqual(
            self.instance.organization,
            self.organization,
        )

        self.assertEqual(
            self.instance.name,
            "HDFC",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the bank_account display string.
        """

        self.assertIn(
            "HDFC",
            str(self.instance),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        BankAccount model should use the configured database table.
        """

        self.assertEqual(
            BankAccount._meta.db_table,
            "cash_management_bank_accounts",
        )


class CashTransactionModelTestCase(BaseTestCase):
    """
    Test cases for the CashTransaction model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()
        self.bank_account = BankAccount.objects.create(
            organization=self.organization,
            name="HDFC",
            account_number="ACC001",
            bank_name="HDFC Bank",
        )

        self.instance = CashTransaction.objects.create(
            organization=self.organization,
            reference="TXN001",
            transaction_type="deposit",
            amount="100.00",
            bank_account=self.bank_account,
        )

    def test_cash_transaction_creation(
        self,
    ) -> None:
        """
        CashTransaction should be created successfully.
        """

        self.assertEqual(
            self.instance.organization,
            self.organization,
        )

        self.assertEqual(
            self.instance.reference,
            "TXN001",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should return the cash_transaction display string.
        """

        self.assertIn(
            "TXN001",
            str(self.instance),
        )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        CashTransaction model should use the configured database table.
        """

        self.assertEqual(
            CashTransaction._meta.db_table,
            "cash_management_cash_transactions",
        )


__all__ = [
    "BankAccountModelTestCase",
    "CashTransactionModelTestCase",
]
