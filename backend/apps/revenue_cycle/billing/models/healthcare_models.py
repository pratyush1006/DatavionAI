from __future__ import annotations

from decimal import Decimal
from uuid import uuid4

from django.db import models


class HealthcareInvoice(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        FINALIZED = "finalized", "Finalized"
        PARTIALLY_PAID = "partially_paid", "Partially Paid"
        PAID = "paid", "Paid"
        VOID = "void", "Void"
        WRITTEN_OFF = "written_off", "Written Off"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="rcm_healthcare_invoices",
    )
    invoice_number = models.CharField(max_length=64)
    patient_reference = models.CharField(max_length=128, blank=True, default="")
    payer_name = models.CharField(max_length=255, blank=True, default="")
    claim_reference = models.CharField(max_length=128, blank=True, default="")
    currency = models.CharField(max_length=3, default="INR")
    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.DRAFT
    )
    subtotal = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    tax_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    discount_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    total = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    paid_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    adjustment_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    balance_due = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    due_date = models.DateField(null=True, blank=True)
    finalized_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "rcm_healthcare_invoices"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "invoice_number"],
                name="rcm_hc_invoice_org_number_uniq",
            )
        ]
        indexes = [
            models.Index(fields=["organization", "status"]),
            models.Index(fields=["organization", "patient_reference"]),
            models.Index(fields=["organization", "claim_reference"]),
        ]

    def recalculate_balance(self):
        self.balance_due = max(
            (self.total - self.paid_total + self.adjustment_total).quantize(
                Decimal("0.01")
            ),
            Decimal("0.00"),
        )
        if self.status not in {
            self.Status.DRAFT,
            self.Status.VOID,
            self.Status.WRITTEN_OFF,
        }:
            if self.balance_due <= Decimal("0.00") and self.total > 0:
                self.status = self.Status.PAID
            elif self.paid_total > 0:
                self.status = self.Status.PARTIALLY_PAID
        return self.balance_due


class HealthcareInvoiceLine(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    invoice = models.ForeignKey(
        HealthcareInvoice, on_delete=models.PROTECT, related_name="lines"
    )
    service_code = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    quantity = models.DecimalField(
        max_digits=18, decimal_places=4, default=Decimal("1.0000")
    )
    unit_price = models.DecimalField(max_digits=18, decimal_places=2)
    discount_amount = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    tax_amount = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    line_total = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rcm_healthcare_invoice_lines"

    def calculate_total(self):
        self.line_total = max(
            (
                self.quantity * self.unit_price - self.discount_amount + self.tax_amount
            ).quantize(Decimal("0.01")),
            Decimal("0.00"),
        )
        return self.line_total


class HealthcarePayment(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        POSTED = "posted", "Posted"
        VOID = "void", "Void"
        REFUNDED = "refunded", "Refunded"

    class Method(models.TextChoices):
        CASH = "cash", "Cash"
        CARD = "card", "Card"
        BANK = "bank", "Bank Transfer"
        UPI = "upi", "UPI"
        INSURANCE = "insurance", "Insurance"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="rcm_healthcare_payments",
    )
    invoice = models.ForeignKey(
        HealthcareInvoice, on_delete=models.PROTECT, related_name="payments"
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    method = models.CharField(max_length=32, choices=Method.choices)
    reference = models.CharField(max_length=128, blank=True, default="")
    gateway_order_id = models.CharField(
        max_length=128, blank=True, default="", db_index=True
    )
    gateway_payment_id = models.CharField(
        max_length=128, blank=True, default="", db_index=True
    )
    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.POSTED
    )
    posted_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rcm_healthcare_payments"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "reference"],
                name="rcm_hc_payment_org_reference_uniq",
            )
        ]


class HealthcarePaymentAllocation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="rcm_healthcare_payment_allocations",
    )
    payment = models.ForeignKey(
        HealthcarePayment, on_delete=models.PROTECT, related_name="allocations"
    )
    invoice = models.ForeignKey(
        HealthcareInvoice, on_delete=models.PROTECT, related_name="payment_allocations"
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rcm_healthcare_payment_allocations"


class HealthcareAdjustment(models.Model):
    class Reason(models.TextChoices):
        CONTRACTUAL = "contractual", "Contractual"
        DISCOUNT = "discount", "Discount"
        BAD_DEBT = "bad_debt", "Bad Debt"
        REFUND = "refund", "Refund"
        OTHER = "other", "Other"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="rcm_healthcare_adjustments",
    )
    invoice = models.ForeignKey(
        HealthcareInvoice, on_delete=models.PROTECT, related_name="adjustments"
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    reason = models.CharField(max_length=32, choices=Reason.choices)
    reference = models.CharField(max_length=128, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rcm_healthcare_adjustments"


class HealthcareRefund(models.Model):
    class Status(models.TextChoices):
        REQUESTED = "requested", "Requested"
        APPROVED = "approved", "Approved"
        PROCESSED = "processed", "Processed"
        REJECTED = "rejected", "Rejected"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="rcm_healthcare_refunds",
    )
    payment = models.ForeignKey(
        HealthcarePayment, on_delete=models.PROTECT, related_name="refunds"
    )
    amount = models.DecimalField(max_digits=18, decimal_places=2)
    reason = models.CharField(max_length=500)
    status = models.CharField(
        max_length=32, choices=Status.choices, default=Status.REQUESTED
    )
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "rcm_healthcare_refunds"


class HealthcareStatement(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="rcm_healthcare_statements",
    )
    patient_reference = models.CharField(max_length=128)
    period_start = models.DateField()
    period_end = models.DateField()
    opening_balance = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    charges = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    payments = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    adjustments = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    closing_balance = models.DecimalField(
        max_digits=18, decimal_places=2, default=Decimal("0.00")
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rcm_healthcare_statements"
        indexes = [models.Index(fields=["organization", "patient_reference"])]


class HealthcareBillingAuditLog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="rcm_healthcare_billing_audits",
    )
    event_type = models.CharField(max_length=128)
    object_type = models.CharField(max_length=128)
    object_id = models.CharField(max_length=128)
    payload = models.JSONField(default=dict)
    actor_id = models.CharField(max_length=128, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rcm_healthcare_billing_audit_logs"
        indexes = [
            models.Index(fields=["organization", "event_type"]),
            models.Index(fields=["organization", "object_type", "object_id"]),
        ]


class HealthcareBillingIdempotencyKey(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="rcm_healthcare_billing_idempotency",
    )
    workflow = models.CharField(max_length=160)
    key = models.CharField(max_length=160)
    response_object_type = models.CharField(max_length=128, blank=True, default="")
    response_object_id = models.CharField(max_length=128, blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rcm_healthcare_billing_idempotency"
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "workflow", "key"], name="rcm_hc_bill_idem_uniq"
            )
        ]


class HealthcareBillingOutboxEvent(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PROCESSING = "processing", "Processing"
        PUBLISHED = "published", "Published"
        FAILED = "failed", "Failed"

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.PROTECT,
        related_name="rcm_healthcare_billing_outbox",
    )
    event_id = models.UUIDField(default=uuid4, unique=True, editable=False)
    event_type = models.CharField(max_length=128)
    aggregate_type = models.CharField(max_length=128)
    aggregate_id = models.CharField(max_length=128)
    payload = models.JSONField(default=dict)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING
    )
    attempts = models.PositiveIntegerField(default=0)
    available_at = models.DateTimeField(auto_now_add=True)
    published_at = models.DateTimeField(null=True, blank=True)
    last_error = models.TextField(blank=True, default="")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "rcm_healthcare_billing_outbox"
        indexes = [models.Index(fields=["organization", "status", "available_at"])]
