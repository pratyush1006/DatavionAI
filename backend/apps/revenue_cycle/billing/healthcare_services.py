from __future__ import annotations

from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction
from django.utils import timezone

from .healthcare_models import (
    HealthcareAdjustment,
    HealthcareBillingAuditLog,
    HealthcareBillingOutboxEvent,
    HealthcareInvoice,
    HealthcareInvoiceLine,
    HealthcarePayment,
    HealthcarePaymentAllocation,
    HealthcareRefund,
    HealthcareStatement,
)


def _audit(org, event_type, obj, payload=None, actor=None):
    return HealthcareBillingAuditLog.objects.create(
        organization=org,
        event_type=event_type,
        object_type=obj.__class__.__name__,
        object_id=str(obj.pk),
        payload=payload or {},
        actor_id=str(getattr(actor, "pk", actor) or ""),
    )


def _event(org, event_type, obj, payload=None):
    return HealthcareBillingOutboxEvent.objects.create(
        organization=org,
        event_type=event_type,
        aggregate_type=obj.__class__.__name__,
        aggregate_id=str(obj.pk),
        payload=payload or {},
    )


def create_invoice(
    *,
    organization,
    invoice_number,
    lines,
    patient_reference="",
    payer_name="",
    claim_reference="",
    due_date=None,
    actor=None,
):
    if not lines:
        raise ValidationError("At least one invoice line is required.")
    with transaction.atomic():
        invoice = HealthcareInvoice.objects.create(
            organization=organization,
            invoice_number=invoice_number,
            patient_reference=patient_reference,
            payer_name=payer_name,
            claim_reference=claim_reference,
            due_date=due_date,
        )
        subtotal = tax = discount = Decimal("0.00")
        for item in lines:
            line = HealthcareInvoiceLine(invoice=invoice, **item)
            if line.quantity <= 0 or line.unit_price < 0:
                raise ValidationError(
                    "Invoice quantity must be positive and unit price cannot be negative."
                )
            line.calculate_total()
            line.save()
            subtotal += (
                Decimal(str(line.quantity)) * Decimal(str(line.unit_price))
            ).quantize(Decimal("0.01"))
            discount += line.discount_amount
            tax += line.tax_amount
        invoice.subtotal = subtotal
        invoice.discount_total = discount
        invoice.tax_total = tax
        invoice.total = max(subtotal - discount + tax, Decimal("0.00"))
        invoice.balance_due = invoice.total
        invoice.save(
            update_fields=[
                "subtotal",
                "discount_total",
                "tax_total",
                "total",
                "balance_due",
                "updated_at",
            ]
        )
        _audit(
            organization,
            "invoice.created",
            invoice,
            {"total": str(invoice.total)},
            actor,
        )
        _event(
            organization,
            "rcm.healthcare_billing.invoice_created",
            invoice,
            {"invoice_id": str(invoice.pk), "total": str(invoice.total)},
        )
        return invoice


def finalize_invoice(*, organization, invoice, actor=None):
    with transaction.atomic():
        invoice = HealthcareInvoice.objects.select_for_update().get(
            pk=invoice.pk, organization=organization
        )
        if invoice.status != HealthcareInvoice.Status.DRAFT:
            raise ValidationError("Only draft invoices can be finalized.")
        if not invoice.lines.exists():
            raise ValidationError("Invoice requires at least one line.")
        invoice.status = HealthcareInvoice.Status.FINALIZED
        invoice.finalized_at = timezone.now()
        invoice.save(update_fields=["status", "finalized_at", "updated_at"])
        _audit(organization, "invoice.finalized", invoice, {}, actor)
        _event(
            organization,
            "rcm.healthcare_billing.invoice_finalized",
            invoice,
            {"invoice_id": str(invoice.pk)},
        )
        return invoice


def post_payment(*, organization, invoice, amount, method, reference, actor=None):
    amount = Decimal(str(amount)).quantize(Decimal("0.01"))
    if amount <= 0:
        raise ValidationError("Payment amount must be positive.")
    with transaction.atomic():
        invoice = HealthcareInvoice.objects.select_for_update().get(
            pk=invoice.pk, organization=organization
        )
        if invoice.status in {
            HealthcareInvoice.Status.DRAFT,
            HealthcareInvoice.Status.VOID,
        }:
            raise ValidationError("Invoice must be finalized before payment.")
        if amount > invoice.balance_due:
            raise ValidationError("Payment exceeds invoice balance.")
        payment = HealthcarePayment.objects.create(
            organization=organization,
            invoice=invoice,
            amount=amount,
            method=method,
            reference=reference,
        )
        HealthcarePaymentAllocation.objects.create(
            organization=organization, payment=payment, invoice=invoice, amount=amount
        )
        invoice.paid_total += amount
        invoice.recalculate_balance()
        invoice.save(
            update_fields=["paid_total", "balance_due", "status", "updated_at"]
        )
        _audit(
            organization,
            "payment.posted",
            payment,
            {"invoice_id": str(invoice.pk), "amount": str(amount)},
            actor,
        )
        _event(
            organization,
            "rcm.healthcare_billing.payment_posted",
            payment,
            {"invoice_id": str(invoice.pk), "amount": str(amount)},
        )
        return payment


def create_pending_payment(
    *, organization, invoice, amount, method, gateway_order_id, actor=None
):
    """Record an external checkout order without crediting the invoice yet."""

    amount = Decimal(str(amount)).quantize(Decimal("0.01"))
    if amount <= 0 or not gateway_order_id:
        raise ValidationError("A positive payment and gateway order are required.")
    with transaction.atomic():
        invoice = HealthcareInvoice.objects.select_for_update().get(
            pk=invoice.pk, organization=organization
        )
        if invoice.status in {
            HealthcareInvoice.Status.DRAFT,
            HealthcareInvoice.Status.VOID,
        }:
            raise ValidationError("Invoice must be finalized before payment.")
        if amount > invoice.balance_due:
            raise ValidationError("Payment exceeds invoice balance.")
        existing = HealthcarePayment.objects.filter(
            organization=organization,
            gateway_order_id=gateway_order_id,
        ).first()
        if existing:
            return existing
        payment = HealthcarePayment.objects.create(
            organization=organization,
            invoice=invoice,
            amount=amount,
            method=method,
            reference=gateway_order_id,
            gateway_order_id=gateway_order_id,
            status=HealthcarePayment.Status.PENDING,
        )
        _audit(
            organization,
            "payment.order_created",
            payment,
            {"invoice_id": str(invoice.pk), "amount": str(amount)},
            actor,
        )
        _event(
            organization,
            "rcm.healthcare_billing.payment_order_created",
            payment,
            {"invoice_id": str(invoice.pk), "amount": str(amount)},
        )
        return payment


def settle_pending_payment(
    *, organization, payment, gateway_payment_id, method=None, actor=None
):
    """Settle a verified gateway payment and allocate it to its RCM invoice."""

    if not gateway_payment_id:
        raise ValidationError("Gateway payment ID is required.")
    with transaction.atomic():
        payment = HealthcarePayment.objects.select_for_update().get(
            pk=payment.pk, organization=organization
        )
        invoice = HealthcareInvoice.objects.select_for_update().get(
            pk=payment.invoice_id, organization=organization
        )
        if payment.status == HealthcarePayment.Status.POSTED:
            if payment.gateway_payment_id == gateway_payment_id:
                return payment
            raise ValidationError("Payment order was already settled differently.")
        if payment.status != HealthcarePayment.Status.PENDING:
            raise ValidationError("Only pending payment orders can be settled.")
        if payment.amount > invoice.balance_due:
            raise ValidationError("Payment exceeds invoice balance.")
        payment.status = HealthcarePayment.Status.POSTED
        payment.gateway_payment_id = gateway_payment_id
        if method:
            payment.method = method
        payment.save(
            update_fields=["status", "gateway_payment_id", "method"],
        )
        HealthcarePaymentAllocation.objects.create(
            organization=organization,
            payment=payment,
            invoice=invoice,
            amount=payment.amount,
        )
        invoice.paid_total += payment.amount
        invoice.recalculate_balance()
        invoice.save(
            update_fields=["paid_total", "balance_due", "status", "updated_at"],
        )
        _audit(
            organization,
            "payment.posted",
            payment,
            {"invoice_id": str(invoice.pk), "amount": str(payment.amount)},
            actor,
        )
        _event(
            organization,
            "rcm.healthcare_billing.payment_posted",
            payment,
            {"invoice_id": str(invoice.pk), "amount": str(payment.amount)},
        )
        return payment


def apply_adjustment(
    *, organization, invoice, amount, reason, reference="", actor=None
):
    amount = Decimal(str(amount)).quantize(Decimal("0.01"))
    if amount == 0:
        raise ValidationError("Adjustment cannot be zero.")
    with transaction.atomic():
        invoice = HealthcareInvoice.objects.select_for_update().get(
            pk=invoice.pk, organization=organization
        )
        adjustment = HealthcareAdjustment.objects.create(
            organization=organization,
            invoice=invoice,
            amount=amount,
            reason=reason,
            reference=reference,
        )
        invoice.adjustment_total += amount
        invoice.recalculate_balance()
        invoice.save(
            update_fields=["adjustment_total", "balance_due", "status", "updated_at"]
        )
        _audit(
            organization,
            "invoice.adjusted",
            adjustment,
            {"invoice_id": str(invoice.pk), "amount": str(amount)},
            actor,
        )
        _event(
            organization,
            "rcm.healthcare_billing.invoice_adjusted",
            adjustment,
            {"invoice_id": str(invoice.pk), "amount": str(amount)},
        )
        return adjustment


def request_refund(*, organization, payment, amount, reason, actor=None):
    amount = Decimal(str(amount)).quantize(Decimal("0.01"))
    if amount <= 0 or amount > payment.amount:
        raise ValidationError(
            "Refund amount must be positive and cannot exceed payment."
        )
    refund = HealthcareRefund.objects.create(
        organization=organization, payment=payment, amount=amount, reason=reason
    )
    _audit(
        organization,
        "refund.requested",
        refund,
        {"payment_id": str(payment.pk), "amount": str(amount)},
        actor,
    )
    _event(
        organization,
        "rcm.healthcare_billing.refund_requested",
        refund,
        {"payment_id": str(payment.pk), "amount": str(amount)},
    )
    return refund


def approve_refund(*, organization, refund, actor=None):
    with transaction.atomic():
        refund = HealthcareRefund.objects.select_for_update().get(
            pk=refund.pk, organization=organization
        )
        if refund.status != HealthcareRefund.Status.REQUESTED:
            raise ValidationError("Only requested refunds can be approved.")
        refund.status = HealthcareRefund.Status.APPROVED
        refund.save(update_fields=["status"])
        _audit(organization, "refund.approved", refund, {}, actor)
        _event(organization, "rcm.healthcare_billing.refund_approved", refund, {})
        return refund


def process_refund(*, organization, refund, actor=None):
    with transaction.atomic():
        refund = HealthcareRefund.objects.select_for_update().get(
            pk=refund.pk, organization=organization
        )
        if refund.status != HealthcareRefund.Status.APPROVED:
            raise ValidationError("Refund must be approved before processing.")
        refund.status = HealthcareRefund.Status.PROCESSED
        refund.processed_at = timezone.now()
        refund.save(update_fields=["status", "processed_at"])
        invoice = HealthcareInvoice.objects.select_for_update().get(
            pk=refund.payment.invoice_id, organization=organization
        )
        invoice.paid_total -= refund.amount
        invoice.recalculate_balance()
        invoice.save(
            update_fields=["paid_total", "balance_due", "status", "updated_at"]
        )
        _audit(organization, "refund.processed", refund, {}, actor)
        _event(organization, "rcm.healthcare_billing.refund_processed", refund, {})
        return refund


def generate_statement(*, organization, patient_reference, period_start, period_end):
    qs = HealthcareInvoice.objects.filter(
        organization=organization,
        patient_reference=patient_reference,
        finalized_at__date__gte=period_start,
        finalized_at__date__lte=period_end,
    ).exclude(status=HealthcareInvoice.Status.VOID)
    charges = sum((x.total for x in qs), Decimal("0.00"))
    payments = sum((x.paid_total for x in qs), Decimal("0.00"))
    adjustments = sum((x.adjustment_total for x in qs), Decimal("0.00"))
    statement = HealthcareStatement.objects.create(
        organization=organization,
        patient_reference=patient_reference,
        period_start=period_start,
        period_end=period_end,
        charges=charges,
        payments=payments,
        adjustments=adjustments,
        closing_balance=charges - payments + adjustments,
    )
    _audit(
        organization,
        "statement.generated",
        statement,
        {"patient_reference": patient_reference},
    )
    _event(
        organization,
        "rcm.healthcare_billing.statement_generated",
        statement,
        {"statement_id": str(statement.pk)},
    )
    return statement
