import os
import subprocess
import sys
from pathlib import Path

from django.conf import settings
from django.test import SimpleTestCase
from django.urls import resolve

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT.parents[2]


class FinanceProductionHardeningTests(SimpleTestCase):
    def test_migration_drift_is_clean(self):
        result = subprocess.run(
            [
                sys.executable,
                "manage.py",
                "makemigrations",
                "finance",
                "--check",
                "--dry-run",
                "--noinput",
            ],
            cwd=str(BACKEND),
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("Migrations for 'finance'", result.stdout + result.stderr)

    def test_no_stale_finance_platform_wiring_remains(self):
        settings_module = os.environ.get("DJANGO_SETTINGS_MODULE")
        self.assertTrue(settings_module)
        settings_path = BACKEND / Path(*settings_module.split(".")).with_suffix(".py")
        source = settings_path.read_text(encoding="utf-8")
        self.assertNotIn("finance_platform", source)
        url_module = __import__(settings.ROOT_URLCONF, fromlist=["*"])
        url_source = Path(url_module.__file__).read_text(encoding="utf-8")
        self.assertNotIn("finance_platform", url_source)
        self.assertIn("apps.billing.finance.api.urls", url_source)

    def test_root_api_route_resolves(self):
        match = resolve("/api/finance/health/")
        self.assertEqual(match.url_name, "finance-health")

    def test_api_views_require_authentication_and_tenant_scope(self):
        source = (ROOT / "api" / "views.py").read_text(encoding="utf-8")
        self.assertGreaterEqual(
            source.count("permission_classes = (IsAuthenticated,)"), 3
        )
        self.assertGreaterEqual(source.count("organization_from(request)"), 5)
        self.assertIn("organization=organization_from(request)", source)

    def test_api_detail_queries_are_organization_scoped(self):
        source = (ROOT / "api" / "views.py").read_text(encoding="utf-8")
        self.assertNotIn(".objects.get(id=object_id)", source)
        self.assertIn(
            "filter(id=object_id, organization=organization_from(request))", source
        )

    def test_finance_tables_are_namespaced(self):
        from apps.billing.finance.models import (
            BankAccount,
            Budget,
            CashTransaction,
            FinanceAuditLog,
            FinanceIdempotencyKey,
            FinanceOutboxEvent,
            FinancialReport,
            FiscalPeriod,
            JournalEntry,
            JournalLine,
            LedgerAccount,
            TaxFiling,
            TaxRate,
            Vendor,
            VendorInvoice,
        )

        models = (
            BankAccount,
            Budget,
            CashTransaction,
            FinanceAuditLog,
            FinanceIdempotencyKey,
            FinanceOutboxEvent,
            FinancialReport,
            FiscalPeriod,
            JournalEntry,
            LedgerAccount,
            JournalLine,
            TaxFiling,
            TaxRate,
            Vendor,
            VendorInvoice,
        )
        for model in models:
            self.assertTrue(model._meta.db_table.startswith("finance_"), model.__name__)

    def test_double_entry_has_expected_numeric_precision(self):
        from apps.billing.finance.models import JournalEntry, JournalLine

        self.assertEqual(JournalEntry._meta.get_field("total_debit").decimal_places, 2)
        self.assertEqual(JournalEntry._meta.get_field("total_credit").decimal_places, 2)
        self.assertEqual(JournalLine._meta.get_field("debit").decimal_places, 2)
        self.assertEqual(JournalLine._meta.get_field("credit").decimal_places, 2)

    def test_management_command_is_registered(self):
        from django.core.management import get_commands

        owner = get_commands().get("publish_finance_events")
        self.assertIn(owner, {"finance", "apps.billing.finance"})

        from importlib import import_module

        module = import_module(f"{owner}.management.commands.publish_finance_events")
        self.assertTrue(hasattr(module, "Command"))
        self.assertTrue(callable(module.Command))
