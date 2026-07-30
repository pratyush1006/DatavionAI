"""
Tests for the General Ledger models.
"""

from __future__ import annotations

from datetime import datetime

from django.db import IntegrityError

from apps.billing.general_ledger.constants import (
    AccountStatus,
    AccountType,
)
from apps.billing.general_ledger.models import (
    GeneralLedgerAccount,
    GeneralLedgerJournalEntry,
)
from apps.common.tests.base import BaseTestCase


class GeneralLedgerAccountModelTestCase(BaseTestCase):
    """
    Test cases for the GeneralLedgerAccount model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.account = GeneralLedgerAccount.objects.create(
            organization=self.organization,
            code="1000",
            name="Cash Account",
            account_type=AccountType.ASSET,
            status=AccountStatus.ACTIVE,
        )

    def test_account_creation(
        self,
    ) -> None:
        """
        Account should be created successfully.
        """

        self.assertEqual(
            self.account.organization,
            self.organization,
        )

        self.assertEqual(
            self.account.code,
            "1000",
        )

        self.assertEqual(
            self.account.account_type,
            AccountType.ASSET,
        )

    def test_default_status(
        self,
    ) -> None:
        """
        Default account status should be active.
        """

        account = GeneralLedgerAccount.objects.create(
            organization=self.organization,
            code="2000",
            name="Revenue Account",
            account_type=AccountType.REVENUE,
        )

        self.assertEqual(
            account.status,
            AccountStatus.ACTIVE,
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should include code and name.
        """

        self.assertIn(
            "1000",
            str(self.account),
        )

        self.assertIn(
            "Cash Account",
            str(self.account),
        )

    def test_unique_code_per_organization(
        self,
    ) -> None:
        """
        Account code should be unique per organization.
        """

        with self.assertRaises(
            IntegrityError,
        ):
            GeneralLedgerAccount.objects.create(
                organization=self.organization,
                code="1000",
                name="Duplicate Account",
                account_type=AccountType.ASSET,
            )

    def test_meta_table_name(
        self,
    ) -> None:
        """
        Model should use the configured database table.
        """

        self.assertEqual(
            GeneralLedgerAccount._meta.db_table,
            "general_ledger_accounts",
        )


class GeneralLedgerJournalEntryModelTestCase(BaseTestCase):
    """
    Test cases for the GeneralLedgerJournalEntry model.
    """

    def setUp(
        self,
    ) -> None:
        super().setUp()

        self.account = GeneralLedgerAccount.objects.create(
            organization=self.organization,
            code="1000",
            name="Cash Account",
            account_type=AccountType.ASSET,
        )

        self.entry = GeneralLedgerJournalEntry.objects.create(
            organization=self.organization,
            account=self.account,
            reference="JE000001",
            entry_type="debit",
            amount="500.00",
            posted_at=datetime(
                2025,
                1,
                1,
            ),
        )

    def test_journal_entry_creation(
        self,
    ) -> None:
        """
        Journal entry should be created successfully.
        """

        self.assertEqual(
            self.entry.account,
            self.account,
        )

        self.assertEqual(
            self.entry.reference,
            "JE000001",
        )

    def test_string_representation(
        self,
    ) -> None:
        """
        __str__ should include reference and entry type.
        """

        self.assertIn(
            "JE000001",
            str(self.entry),
        )


__all__ = [
    "GeneralLedgerAccountModelTestCase",
    "GeneralLedgerJournalEntryModelTestCase",
]
