from __future__ import annotations

from datetime import date, timedelta
from decimal import Decimal
from uuid import uuid4

from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.test import TestCase

from apps.revenue_cycle.billing.healthcare_models import *
from apps.revenue_cycle.billing.healthcare_services import *


def scalar(field, token):
    n = field.name.lower()
    if n in {"name", "legal_name", "display_name"}:
        return f"Billing {token}"
    if n in {"code", "slug", "organization_code"}:
        return f"bill-{token}".lower()
    if "email" in n:
        return f"billing-{token}@example.com"
    if n in {"status", "state"}:
        return "active"
    if n in {"type", "organization_type"}:
        return "healthcare_provider"
    if n in {"size", "organization_size"}:
        return "small"
    if "country" in n:
        return "India"
    if "timezone" in n:
        return "Asia/Kolkata"
    if "currency" in n:
        return "INR"
    if field.get_internal_type() in {"CharField", "TextField"}:
        return (
            token[: field.max_length] if getattr(field, "max_length", None) else token
        )
    if field.get_internal_type() == "BooleanField":
        return True
    if field.get_internal_type() in {
        "IntegerField",
        "BigIntegerField",
        "PositiveIntegerField",
        "PositiveSmallIntegerField",
    }:
        return 1
    return None


def required(model, token, cache=None):
    cache = cache or {}
    if model in cache:
        return cache[model]
    kwargs = {}
    for f in model._meta.fields:
        if (
            f.primary_key
            or f.name in {"created_at", "updated_at"}
            or getattr(f, "auto_now", False)
            or getattr(f, "auto_now_add", False)
            or f.has_default()
            or f.null
            or f.blank
        ):
            continue
        if f.remote_field is not None:
            kwargs[f.name] = required(f.remote_field.model, token, cache)
        else:
            v = scalar(f, token)
            if v is not None:
                kwargs[f.name] = v
    obj = model.objects.create(**kwargs)
    cache[model] = obj
    return obj


def make_org(token):
    from apps.platform.organizations.models import Organization

    return required(Organization, token)


class HealthcareBillingEndToEndTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.org_a = make_org("rcm-a-" + uuid4().hex[:6])
        cls.org_b = make_org("rcm-b-" + uuid4().hex[:6])

    def invoice(self, no="1", amount="1000", patient="P-1"):
        return create_invoice(
            organization=self.org_a,
            invoice_number=f"INV-{no}-{uuid4().hex[:5]}",
            patient_reference=patient,
            claim_reference="CLM-" + no,
            lines=[
                {
                    "service_code": "CONSULT",
                    "description": "Consultation",
                    "quantity": 1,
                    "unit_price": Decimal(amount),
                    "tax_amount": Decimal("0.00"),
                }
            ],
        )

    def test_invoice_creation_totals(self):
        inv = self.invoice(amount="1200")
        self.assertEqual(inv.total, Decimal("1200.00"))
        self.assertEqual(inv.balance_due, Decimal("1200.00"))

    def test_invoice_requires_line(self):
        with self.assertRaises(ValidationError):
            create_invoice(organization=self.org_a, invoice_number="EMPTY", lines=[])

    def test_invoice_finalize(self):
        inv = self.invoice()
        finalize_invoice(organization=self.org_a, invoice=inv)
        inv.refresh_from_db()
        self.assertEqual(inv.status, HealthcareInvoice.Status.FINALIZED)
        self.assertIsNotNone(inv.finalized_at)

    def test_draft_payment_rejected(self):
        inv = self.invoice()
        with self.assertRaises(ValidationError):
            post_payment(
                organization=self.org_a,
                invoice=inv,
                amount=10,
                method="cash",
                reference="DRAFT-PAY",
            )

    def test_partial_and_full_payment(self):
        inv = self.invoice(amount="500")
        finalize_invoice(organization=self.org_a, invoice=inv)
        post_payment(
            organization=self.org_a,
            invoice=inv,
            amount=200,
            method="cash",
            reference="P1",
        )
        inv.refresh_from_db()
        self.assertEqual(inv.balance_due, Decimal("300.00"))
        post_payment(
            organization=self.org_a,
            invoice=inv,
            amount=300,
            method="upi",
            reference="P2",
        )
        inv.refresh_from_db()
        self.assertEqual(inv.status, HealthcareInvoice.Status.PAID)
        self.assertEqual(inv.balance_due, Decimal("0.00"))

    def test_gateway_payment_posts_only_after_verified_settlement(self):
        invoice = self.invoice(amount="1000")
        finalize_invoice(organization=self.org_a, invoice=invoice)
        payment = create_pending_payment(
            organization=self.org_a,
            invoice=invoice,
            amount=500,
            method=HealthcarePayment.Method.OTHER,
            gateway_order_id="order_rcm_test_001",
        )

        invoice.refresh_from_db()
        self.assertEqual(invoice.paid_total, Decimal("0.00"))
        self.assertEqual(payment.status, HealthcarePayment.Status.PENDING)

        settled = settle_pending_payment(
            organization=self.org_a,
            payment=payment,
            gateway_payment_id="pay_rcm_test_001",
        )
        replayed = settle_pending_payment(
            organization=self.org_a,
            payment=payment,
            gateway_payment_id="pay_rcm_test_001",
        )

        invoice.refresh_from_db()
        self.assertEqual(settled.status, HealthcarePayment.Status.POSTED)
        self.assertEqual(replayed.pk, payment.pk)
        self.assertEqual(invoice.paid_total, Decimal("500.00"))
        self.assertEqual(invoice.balance_due, Decimal("500.00"))
        self.assertEqual(payment.allocations.count(), 1)

    def test_overpayment_rejected(self):
        inv = self.invoice(amount="100")
        finalize_invoice(organization=self.org_a, invoice=inv)
        with self.assertRaises(ValidationError):
            post_payment(
                organization=self.org_a,
                invoice=inv,
                amount=101,
                method="card",
                reference="OVER",
            )

    def test_adjustment_updates_balance(self):
        inv = self.invoice(amount="1000")
        finalize_invoice(organization=self.org_a, invoice=inv)
        apply_adjustment(
            organization=self.org_a, invoice=inv, amount="-100", reason="discount"
        )
        inv.refresh_from_db()
        self.assertEqual(inv.balance_due, Decimal("900.00"))

    def test_negative_adjustment_and_positive_adjustment_allowed(self):
        inv = self.invoice(amount="1000")
        finalize_invoice(organization=self.org_a, invoice=inv)
        apply_adjustment(
            organization=self.org_a, invoice=inv, amount="100", reason="other"
        )
        inv.refresh_from_db()
        self.assertEqual(inv.balance_due, Decimal("1100.00"))

    def test_refund_workflow(self):
        inv = self.invoice(amount="1000")
        finalize_invoice(organization=self.org_a, invoice=inv)
        payment = post_payment(
            organization=self.org_a,
            invoice=inv,
            amount=1000,
            method="card",
            reference="REF-PAY",
        )
        refund = request_refund(
            organization=self.org_a, payment=payment, amount=250, reason="duplicate"
        )
        with self.assertRaises(ValidationError):
            process_refund(organization=self.org_a, refund=refund)
        approve_refund(organization=self.org_a, refund=refund)
        process_refund(organization=self.org_a, refund=refund)
        inv.refresh_from_db()
        refund.refresh_from_db()
        self.assertEqual(inv.balance_due, Decimal("250.00"))
        self.assertEqual(refund.status, HealthcareRefund.Status.PROCESSED)

    def test_refund_amount_cannot_exceed_payment(self):
        inv = self.invoice(amount="100")
        finalize_invoice(organization=self.org_a, invoice=inv)
        pay = post_payment(
            organization=self.org_a,
            invoice=inv,
            amount=100,
            method="cash",
            reference="RF-OVER",
        )
        with self.assertRaises(ValidationError):
            request_refund(
                organization=self.org_a, payment=pay, amount=101, reason="invalid"
            )

    def test_statement_generation(self):
        inv = self.invoice(amount="600", patient="PAT-ST")
        finalize_invoice(organization=self.org_a, invoice=inv)
        post_payment(
            organization=self.org_a,
            invoice=inv,
            amount=200,
            method="upi",
            reference="ST-PAY",
        )
        s = generate_statement(
            organization=self.org_a,
            patient_reference="PAT-ST",
            period_start=date.today() - timedelta(days=2),
            period_end=date.today() + timedelta(days=2),
        )
        self.assertEqual(s.charges, Decimal("600.00"))
        self.assertEqual(s.payments, Decimal("200.00"))
        self.assertEqual(s.closing_balance, Decimal("400.00"))

    def test_cross_tenant_isolation(self):
        inv = self.invoice()
        with self.assertRaises(HealthcareInvoice.DoesNotExist):
            HealthcareInvoice.objects.get(pk=inv.pk, organization=self.org_b)

    def test_duplicate_invoice_number_blocked(self):
        no = "DUP-" + uuid4().hex[:5]
        self.assertEqual(
            HealthcareInvoice.objects.filter(
                organization=self.org_a, invoice_number=no
            ).count(),
            0,
        )
        create_invoice(
            organization=self.org_a,
            invoice_number=no,
            patient_reference="P-DUP",
            claim_reference="CLM-DUP",
            lines=[
                {
                    "service_code": "CONSULT",
                    "description": "Consultation",
                    "quantity": 1,
                    "unit_price": Decimal("100.00"),
                    "tax_amount": Decimal("0.00"),
                }
            ],
        )
        with self.assertRaises(IntegrityError):
            create_invoice(
                organization=self.org_a,
                invoice_number=no,
                patient_reference="P-DUP2",
                claim_reference="CLM-DUP2",
                lines=[
                    {
                        "service_code": "CONSULT",
                        "description": "Consultation",
                        "quantity": 1,
                        "unit_price": Decimal("100.00"),
                        "tax_amount": Decimal("0.00"),
                    }
                ],
            )

    def test_duplicate_payment_reference_blocked(self):
        inv = self.invoice()
        finalize_invoice(organization=self.org_a, invoice=inv)
        post_payment(
            organization=self.org_a,
            invoice=inv,
            amount=10,
            method="cash",
            reference="DUP-PAY",
        )
        with self.assertRaises(IntegrityError):
            post_payment(
                organization=self.org_a,
                invoice=inv,
                amount=10,
                method="cash",
                reference="DUP-PAY",
            )

    def test_audit_and_outbox_for_invoice(self):
        inv = self.invoice()
        self.assertTrue(
            HealthcareBillingAuditLog.objects.filter(
                organization=self.org_a,
                object_id=str(inv.pk),
                event_type="invoice.created",
            ).exists()
        )
        self.assertTrue(
            HealthcareBillingOutboxEvent.objects.filter(
                organization=self.org_a,
                aggregate_id=str(inv.pk),
                event_type="rcm.healthcare_billing.invoice_created",
            ).exists()
        )

    def test_idempotency_constraint_is_tenant_scoped(self):
        HealthcareBillingIdempotencyKey.objects.create(
            organization=self.org_a, workflow="create_invoice", key="same"
        )
        HealthcareBillingIdempotencyKey.objects.create(
            organization=self.org_b, workflow="create_invoice", key="same"
        )
        with self.assertRaises(IntegrityError):
            HealthcareBillingIdempotencyKey.objects.create(
                organization=self.org_a, workflow="create_invoice", key="same"
            )

    def test_outbox_is_tenant_scoped(self):
        a = self.invoice()
        b = create_invoice(
            organization=self.org_b,
            invoice_number="B-1",
            lines=[
                {
                    "service_code": "B",
                    "description": "B",
                    "quantity": 1,
                    "unit_price": 100,
                }
            ],
        )
        self.assertTrue(
            HealthcareBillingOutboxEvent.objects.filter(
                organization=self.org_a, aggregate_id=str(a.pk)
            ).exists()
        )
        self.assertTrue(
            HealthcareBillingOutboxEvent.objects.filter(
                organization=self.org_b, aggregate_id=str(b.pk)
            ).exists()
        )
        self.assertEqual(
            HealthcareBillingOutboxEvent.objects.filter(
                organization=self.org_a, aggregate_id=str(b.pk)
            ).count(),
            0,
        )

    def test_workflow_registry(self):
        from apps.revenue_cycle.billing.healthcare_workflows import WORKFLOW_REGISTRY

        for name in (
            "rcm.healthcare_billing.create_invoice",
            "rcm.healthcare_billing.finalize_invoice",
            "rcm.healthcare_billing.post_payment",
            "rcm.healthcare_billing.apply_adjustment",
            "rcm.healthcare_billing.request_refund",
            "rcm.healthcare_billing.approve_refund",
            "rcm.healthcare_billing.process_refund",
        ):
            self.assertIn(name, WORKFLOW_REGISTRY)

    def test_documents_boundary_imports(self):
        from apps.revenue_cycle.billing.document_storage import (
            get_billing_document,
            store_billing_document,
        )

        self.assertTrue(callable(store_billing_document))
        self.assertTrue(callable(get_billing_document))

    def test_management_command_source_exists(self):
        from pathlib import Path

        p = (
            Path(__file__).resolve().parents[1]
            / "management"
            / "commands"
            / "publish_healthcare_billing_events.py"
        )
        self.assertTrue(p.exists())
