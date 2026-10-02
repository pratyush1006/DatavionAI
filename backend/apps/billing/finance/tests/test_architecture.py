import ast
from pathlib import Path

from django.test import SimpleTestCase

from apps.billing.finance.workflows.registry import WORKFLOW_SPECS

ROOT = Path(__file__).resolve().parents[1]


class FreshFinanceArchitectureTests(SimpleTestCase):
    def test_sources_parse(self):
        for path in ROOT.rglob("*.py"):
            ast.parse(path.read_text(encoding="utf-8"), filename=str(path))

    def test_workflow_surface_is_complete(self):
        self.assertGreaterEqual(len(WORKFLOW_SPECS), 22)
        expected = {
            "finance.accounts_payable.create_vendor",
            "finance.accounts_payable.create_vendor_invoice",
            "finance.cash_management.create_bank_account",
            "finance.cash_management.create_cash_transaction",
            "finance.financial_management.create_budget",
            "finance.financial_management.create_financial_report",
            "finance.general_ledger.create_account",
            "finance.general_ledger.open_period",
            "finance.general_ledger.create_journal_entry",
            "finance.general_ledger.post_journal_entry",
            "finance.general_ledger.reverse_journal_entry",
            "finance.tax_gst.create_tax_rate",
            "finance.tax_gst.create_tax_filing",
            "finance.tax_gst.submit_tax_filing",
        }
        self.assertTrue(expected.issubset(WORKFLOW_SPECS))

    def test_double_entry_models(self):
        from apps.billing.finance.models import JournalEntry, JournalLine

        self.assertIsNotNone(JournalEntry)
        self.assertIsNotNone(JournalLine)

    def test_platform_controls_are_persistent(self):
        from apps.billing.finance.models import (
            FinanceAuditLog,
            FinanceIdempotencyKey,
            FinanceOutboxEvent,
        )

        self.assertEqual(FinanceAuditLog._meta.db_table, "finance_core_audit_logs")
        self.assertEqual(
            FinanceIdempotencyKey._meta.db_table, "finance_core_idempotency_keys"
        )
        self.assertEqual(
            FinanceOutboxEvent._meta.db_table, "finance_core_outbox_events"
        )
