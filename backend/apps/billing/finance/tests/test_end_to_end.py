from datetime import date
from decimal import Decimal
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from apps.billing.finance.models import (
    FinanceAuditLog,
    FinanceIdempotencyKey,
    FinanceOutboxEvent,
    LedgerAccount,
    Vendor,
    VendorInvoice,
)
from apps.billing.finance.services import (
    create_bank_account,
    create_budget,
    create_cash_transaction,
    create_financial_report,
    create_journal_entry,
    create_ledger_account,
    create_tax_filing,
    create_tax_rate,
    create_vendor,
    create_vendor_invoice,
    open_fiscal_period,
    post_journal_entry,
    reverse_journal_entry,
    submit_tax_filing,
)
from apps.billing.finance.services.events import enqueue_event, publish_pending_events
from apps.billing.finance.services.idempotency import execute_idempotent


class FinanceEndToEndTests(TestCase):
    @classmethod
    def _scalar_value(cls, field, token, suffix=""):
        internal = field.get_internal_type()
        base = f"finance-test-{token}{suffix}"
        if internal in {"CharField", "TextField", "EmailField", "SlugField"}:
            return base[: getattr(field, "max_length", 254) or 254]
        if internal in {
            "IntegerField",
            "PositiveIntegerField",
            "BigIntegerField",
            "PositiveBigIntegerField",
        }:
            return 1
        if internal == "BooleanField":
            return True
        if internal == "FloatField":
            return 1.0
        if internal == "DecimalField":
            return "1.00"
        return None

    @classmethod
    def _build_required_model(cls, model, token, cache=None, suffix=""):
        cache = cache or {}
        if model in cache:
            return cache[model]
        kwargs = {}
        pending_relations = []
        for field in model._meta.fields:
            if field.name in {"id", "created_at", "updated_at"} or field.primary_key:
                continue
            if getattr(field, "auto_now", False) or getattr(
                field, "auto_now_add", False
            ):
                continue
            if field.has_default() or field.null or field.blank:
                continue
            if field.remote_field is not None:
                pending_relations.append(field)
                continue
            value = cls._scalar_value(field, token, suffix)
            if value is not None:
                kwargs[field.name] = value
        # Populate required foreign-key dependencies before creating the model.
        for field in pending_relations:
            related = field.remote_field.model
            value = cls._build_required_model(
                related, token, cache=cache, suffix=suffix
            )
            kwargs[field.name] = value
        instance = model.objects.create(**kwargs)
        cache[model] = instance
        return instance

    @classmethod
    def _create_organization(cls, Organization, token, suffix=""):
        fields = {}
        dependencies = {}
        cache = {}
        for field in Organization._meta.fields:
            if field.name in {"id", "created_at", "updated_at"} or field.primary_key:
                continue
            if getattr(field, "auto_now", False) or getattr(
                field, "auto_now_add", False
            ):
                continue
            if field.has_default() or field.null or field.blank:
                continue
            if field.remote_field is not None:
                dependencies[field.name] = field.remote_field.model
                continue
            value = cls._scalar_value(field, token, suffix)
            if value is not None:
                fields[field.name] = value
        for name, model in dependencies.items():
            fields[name] = cls._build_required_model(
                model, token, cache=cache, suffix=suffix
            )
        return Organization.objects.create(**fields)

    @classmethod
    def setUpTestData(cls):
        from apps.platform.organizations.models import Organization

        token = uuid4().hex[:10]
        cls.org_a = cls._create_organization(Organization, token, "-a")
        cls.org_b = cls._create_organization(Organization, token, "-b")

    def make_vendor(self, org, suffix="A"):
        return create_vendor(
            organization=org,
            data={
                "code": f"V-{suffix}-{uuid4().hex[:6]}",
                "name": f"Vendor {suffix}",
                "status": "active",
            },
        )

    def make_bank(self, org, suffix="A"):
        return create_bank_account(
            organization=org,
            data={
                "name": f"Bank {suffix}",
                "account_number": f"AC-{suffix}-{uuid4().hex[:8]}",
                "bank_name": "Test Bank",
                "currency": "INR",
                "opening_balance": "1000.00",
            },
        )

    def make_gl(self, org):
        cash = create_ledger_account(
            organization=org,
            data={
                "code": f"1000-{uuid4().hex[:5]}",
                "name": "Cash",
                "account_type": "asset",
                "status": "active",
            },
        )
        revenue = create_ledger_account(
            organization=org,
            data={
                "code": f"4000-{uuid4().hex[:5]}",
                "name": "Revenue",
                "account_type": "income",
                "status": "active",
            },
        )
        period = open_fiscal_period(
            organization=org,
            data={
                "fiscal_year": 2099,
                "period": int(uuid4().hex[:2], 16) % 12 + 1,
                "period_start": date(2099, 1, 1),
                "period_end": date(2099, 12, 31),
                "status": "open",
            },
        )
        return cash, revenue, period

    def test_accounts_payable_vendor_and_invoice_flow(self):
        vendor = self.make_vendor(self.org_a)
        invoice = create_vendor_invoice(
            organization=self.org_a,
            data={
                "vendor_id": str(vendor.id),
                "invoice_number": f"INV-{uuid4().hex[:8]}",
                "reference": "PO-1",
                "invoice_date": date(2099, 1, 1),
                "due_date": date(2099, 2, 1),
                "amount": "100.00",
                "tax_amount": "18.00",
                "status": "draft",
            },
        )
        self.assertEqual(invoice.vendor_id, vendor.id)
        self.assertEqual(
            VendorInvoice.objects.filter(organization=self.org_a).count(), 1
        )

    def test_cross_tenant_vendor_invoice_is_blocked(self):
        vendor = self.make_vendor(self.org_a)
        with self.assertRaises(Vendor.DoesNotExist):
            create_vendor_invoice(
                organization=self.org_b,
                data={
                    "vendor_id": str(vendor.id),
                    "invoice_number": f"X-{uuid4().hex[:8]}",
                    "invoice_date": date(2099, 1, 1),
                    "due_date": date(2099, 2, 1),
                    "amount": "10.00",
                    "status": "draft",
                },
            )

    def test_cash_management_updates_balance_and_immutability(self):
        bank = self.make_bank(self.org_a)
        create_cash_transaction(
            organization=self.org_a,
            data={
                "bank_account_id": str(bank.id),
                "amount": "250.00",
                "transaction_type": "credit",
                "transaction_date": timezone.now(),
                "reference": "RCPT-1",
                "description": "Receipt",
            },
        )
        bank.refresh_from_db()
        self.assertEqual(bank.current_balance, Decimal("1250.00"))
        with self.assertRaises(ValidationError):
            from apps.billing.finance.services import update_cash_transaction

            update_cash_transaction(
                organization=self.org_a, instance_id=uuid4(), data={}
            )

    def test_financial_budget_and_report_lifecycle(self):
        budget = create_budget(
            organization=self.org_a,
            data={
                "name": f"Budget {uuid4().hex[:6]}",
                "fiscal_year": 2099,
                "total_amount": "100000.00",
                "status": "draft",
            },
        )
        report = create_financial_report(
            organization=self.org_a,
            data={
                "title": "Trial Balance",
                "report_type": "trial_balance",
                "period_start": date(2099, 1, 1),
                "period_end": date(2099, 12, 31),
                "status": "draft",
                "budget_id": str(budget.id),
            },
        )
        self.assertEqual(str(report.budget_id), str(budget.id))

    def test_general_ledger_balances_posts_reverses_and_respects_lock(self):
        cash, revenue, period = self.make_gl(self.org_a)
        entry = create_journal_entry(
            organization=self.org_a,
            data={
                "fiscal_period_id": str(period.id),
                "reference": f"JE-{uuid4().hex[:8]}",
                "entry_date": date(2099, 1, 2),
                "lines": [
                    {"account_id": str(cash.id), "debit": "100.00"},
                    {"account_id": str(revenue.id), "credit": "100.00"},
                ],
            },
        )
        self.assertEqual(entry.total_debit, Decimal("100.00"))
        self.assertEqual(entry.total_credit, Decimal("100.00"))
        posted = post_journal_entry(organization=self.org_a, instance_id=entry.id)
        self.assertEqual(posted.status, "posted")
        reversal = reverse_journal_entry(organization=self.org_a, instance_id=entry.id)
        self.assertEqual(reversal.total_debit, Decimal("100.00"))
        entry.refresh_from_db()
        self.assertEqual(entry.status, "reversed")

    def test_unbalanced_journal_is_rejected(self):
        cash, revenue, period = self.make_gl(self.org_a)
        with self.assertRaises(ValidationError):
            create_journal_entry(
                organization=self.org_a,
                data={
                    "fiscal_period_id": str(period.id),
                    "reference": f"BAD-{uuid4().hex[:8]}",
                    "entry_date": date(2099, 1, 2),
                    "lines": [
                        {"account_id": str(cash.id), "debit": "100.00"},
                        {"account_id": str(revenue.id), "credit": "90.00"},
                    ],
                },
            )

    def test_locked_period_rejects_new_entries(self):
        from apps.billing.finance.services import lock_fiscal_period

        cash, revenue, period = self.make_gl(self.org_a)
        lock_fiscal_period(organization=self.org_a, instance_id=period.id)
        with self.assertRaises(ValidationError):
            create_journal_entry(
                organization=self.org_a,
                data={
                    "fiscal_period_id": str(period.id),
                    "reference": f"LOCK-{uuid4().hex[:8]}",
                    "entry_date": date(2099, 1, 2),
                    "lines": [
                        {"account_id": str(cash.id), "debit": "100.00"},
                        {"account_id": str(revenue.id), "credit": "100.00"},
                    ],
                },
            )

    def test_tenant_scoping_for_gl_accounts(self):
        account = create_ledger_account(
            organization=self.org_a,
            data={
                "code": f"A-{uuid4().hex[:6]}",
                "name": "A",
                "account_type": "asset",
                "status": "active",
            },
        )
        with self.assertRaises(LedgerAccount.DoesNotExist):
            LedgerAccount.objects.get(id=account.id, organization=self.org_b)

    def test_tax_rate_filing_and_submission(self):
        rate = create_tax_rate(
            organization=self.org_a,
            data={
                "code": f"GST-{uuid4().hex[:6]}",
                "name": "GST 18",
                "description": "Goods and Services Tax",
                "rate": "18.00",
                "tax_type": "GST",
            },
        )
        filing = create_tax_filing(
            organization=self.org_a,
            data={
                "tax_rate_id": str(rate.id),
                "period": "2099-01",
                "period_start": date(2099, 1, 1),
                "period_end": date(2099, 1, 31),
                "taxable_amount": "1000.00",
                "tax_amount": "180.00",
                "status": "draft",
                "reference": f"GST-{uuid4().hex[:8]}",
            },
        )
        filing = submit_tax_filing(organization=self.org_a, instance_id=filing.id)
        self.assertEqual(filing.status, "submitted")

    def test_idempotency_persists_and_replays(self):
        calls = []

        def execute():
            calls.append(1)
            return self.make_vendor(self.org_a, "IDEMP")

        first, replayed1 = execute_idempotent(
            organization=self.org_a,
            workflow="finance.test.vendor",
            key="same-key",
            execute=execute,
        )
        second, replayed2 = execute_idempotent(
            organization=self.org_a,
            workflow="finance.test.vendor",
            key="same-key",
            execute=execute,
        )
        self.assertFalse(replayed1)
        self.assertTrue(replayed2)
        self.assertEqual(len(calls), 1)
        self.assertEqual(
            FinanceIdempotencyKey.objects.filter(
                organization=self.org_a, key="same-key"
            ).count(),
            1,
        )
        self.assertEqual(str(first.id), second.get("entity_id"))

    def test_workflow_idempotency_audit_and_outbox_are_emitted(self):
        from apps.billing.finance.workflows.registry import get_workflow

        request_key = f"vendor-{uuid4().hex}"
        workflow = get_workflow("finance.accounts_payable.create_vendor")()
        from apps.billing.finance.workflows.base import FinanceWorkflowRequest

        first = workflow.execute(
            None,
            FinanceWorkflowRequest(
                organization=self.org_a,
                payload={
                    "code": f"WF-{uuid4().hex[:6]}",
                    "name": "Workflow Vendor",
                    "status": "active",
                },
                idempotency_key=request_key,
                actor_id=None,
            ),
        )
        second = workflow.execute(
            None,
            FinanceWorkflowRequest(
                organization=self.org_a,
                payload={
                    "code": "SHOULD-NOT-DUP",
                    "name": "Replay",
                    "status": "active",
                },
                idempotency_key=request_key,
                actor_id=None,
            ),
        )
        self.assertFalse(first.metadata["replayed"])
        self.assertTrue(second.metadata["replayed"])
        self.assertEqual(
            FinanceAuditLog.objects.filter(
                organization=self.org_a, workflow=workflow.name
            ).count(),
            1,
        )
        self.assertEqual(
            FinanceOutboxEvent.objects.filter(
                organization=self.org_a, event_type="finance.vendor.created"
            ).count(),
            1,
        )

    def test_outbox_publishes_pending_event(self):
        event = enqueue_event(
            organization=self.org_a,
            event_type="finance.test.event",
            aggregate_type="Vendor",
            payload={"x": 1},
        )
        seen = []
        published = publish_pending_events(limit=10, publisher=seen.append)
        event.refresh_from_db()
        self.assertEqual(published, 1)
        self.assertEqual(event.status, FinanceOutboxEvent.Status.PUBLISHED)
        self.assertEqual(event.attempts, 1)
        self.assertEqual(seen[0]["organization_id"], str(self.org_a.id))

    def test_outbox_retry_after_publisher_failure(self):
        event = enqueue_event(
            organization=self.org_a,
            event_type="finance.retry.event",
            aggregate_type="Vendor",
            payload={},
        )

        def broken(_):
            raise RuntimeError("publisher down")

        publish_pending_events(limit=1, publisher=broken)
        event.refresh_from_db()
        self.assertEqual(event.status, FinanceOutboxEvent.Status.PENDING)
        self.assertEqual(event.attempts, 1)
        self.assertIn("publisher down", event.last_error)

    def test_outbox_retry_exhaustion_moves_to_failed(self):
        event = enqueue_event(
            organization=self.org_a,
            event_type="finance.dlq.event",
            aggregate_type="Vendor",
            payload={},
        )

        def broken(_):
            raise RuntimeError("permanent failure")

        for _ in range(5):
            event.refresh_from_db()
            event.available_at = timezone.now()
            event.save(update_fields=("available_at", "updated_at"))
            publish_pending_events(limit=1, publisher=broken, max_attempts=5)
        event.refresh_from_db()
        self.assertEqual(event.status, FinanceOutboxEvent.Status.FAILED)
        self.assertEqual(event.attempts, 5)
        self.assertIn("permanent failure", event.last_error)

    def test_outbox_is_tenant_scoped(self):
        event = enqueue_event(
            organization=self.org_a,
            event_type="finance.scope.event",
            aggregate_type="Vendor",
            payload={},
        )
        self.assertEqual(
            FinanceOutboxEvent.objects.filter(
                organization=self.org_a, pk=event.pk
            ).count(),
            1,
        )
        self.assertEqual(
            FinanceOutboxEvent.objects.filter(
                organization=self.org_b, pk=event.pk
            ).count(),
            0,
        )

    def test_closed_budget_cannot_be_modified(self):
        budget = create_budget(
            organization=self.org_a,
            data={
                "name": f"Closed-{uuid4().hex[:6]}",
                "fiscal_year": 2099,
                "total_amount": "100.00",
                "status": "closed",
            },
        )
        from apps.billing.finance.services import update_budget

        with self.assertRaises(ValidationError):
            update_budget(
                organization=self.org_a,
                instance_id=budget.id,
                data={"total_amount": "200.00"},
            )

    def test_generated_report_is_immutable(self):
        report = create_financial_report(
            organization=self.org_a,
            data={
                "title": "Generated",
                "report_type": "balance_sheet",
                "period_start": date(2099, 1, 1),
                "period_end": date(2099, 12, 31),
                "status": "generated",
            },
        )
        from apps.billing.finance.services import update_financial_report

        with self.assertRaises(ValidationError):
            update_financial_report(
                organization=self.org_a,
                instance_id=report.id,
                data={"title": "Changed"},
            )

    def test_tax_filing_cannot_submit_twice(self):
        rate = create_tax_rate(
            organization=self.org_a,
            data={
                "code": f"T-{uuid4().hex[:6]}",
                "name": "Tax",
                "rate": "5.00",
                "tax_type": "GST",
            },
        )
        filing = create_tax_filing(
            organization=self.org_a,
            data={
                "tax_rate_id": str(rate.id),
                "period": "2099-02",
                "period_start": date(2099, 2, 1),
                "period_end": date(2099, 2, 28),
                "taxable_amount": "100.00",
                "tax_amount": "5.00",
                "status": "draft",
                "reference": f"F-{uuid4().hex[:6]}",
            },
        )
        submit_tax_filing(organization=self.org_a, instance_id=filing.id)
        with self.assertRaises(ValidationError):
            submit_tax_filing(organization=self.org_a, instance_id=filing.id)

    def test_vendor_update_cannot_cross_tenant(self):
        vendor = self.make_vendor(self.org_a, "A")
        from apps.billing.finance.services import update_vendor

        with self.assertRaises(Vendor.DoesNotExist):
            update_vendor(
                organization=self.org_b,
                instance_id=vendor.id,
                data={"name": "Intruder"},
            )
