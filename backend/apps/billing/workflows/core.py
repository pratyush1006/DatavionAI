"""
Billing Core workflow orchestration.
"""

from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Any
from uuid import UUID

from django.db import transaction

from apps.billing.events import (
    BillingClaimStatusChangedEvent,
    BillingInvoiceCreatedEvent,
    BillingPaymentCreatedEvent,
)
from apps.billing.exceptions import BillingNotFoundError
from apps.billing.models import InsuranceClaim, Invoice
from apps.billing.policies import BillingPolicy
from apps.billing.services import InsuranceClaimService, InvoiceService, PaymentService
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


def _resolve(context: WorkflowContext, organization_id: UUID):
    """Resolve actor, organization, and tenant-scoped data dependencies."""
    try:
        actor = User.objects.get(pk=context.actor_id)
        organization = Organization.objects.get(
            pk=organization_id,
            tenant_id=context.tenant_id,
        )
    except (User.DoesNotExist, Organization.DoesNotExist) as exc:
        raise BillingNotFoundError(
            "Billing actor or organization was not found."
        ) from exc
    return actor, organization


def _patient(organization, patient_id: UUID):
    """Resolve the canonical Patient inside the organization."""
    try:
        return Patient.objects.get(
            pk=patient_id,
            organization_id=organization.pk,
        )
    except Patient.DoesNotExist as exc:
        raise BillingNotFoundError(
            "Patient was not found in the organization."
        ) from exc


def _claim(organization, claim_id: UUID):
    """Resolve an insurance claim inside the organization."""
    try:
        return InsuranceClaim.objects.get(
            pk=claim_id,
            organization_id=organization.pk,
        )
    except InsuranceClaim.DoesNotExist as exc:
        raise BillingNotFoundError("Insurance claim was not found.") from exc


@dataclass(frozen=True, slots=True, kw_only=True)
class InvoiceCreationRequest:
    """Input required for invoice creation."""

    organization_id: UUID
    patient_id: UUID
    data: dict[str, Any]
    items: list[dict[str, Any]]


class InvoiceCreationWorkflow(BaseWorkflow):
    """Create invoices through policy and service boundaries."""

    workflow_name = "billing.invoice.create"

    def __init__(self, *, request: InvoiceCreationRequest, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or BillingPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Create an invoice and publish its event after commit."""
        actor, organization = _resolve(context, self._request.organization_id)
        patient = _patient(organization, self._request.patient_id)
        if not self._policy.can_create_invoice(actor=actor, organization=organization):
            raise PermissionError("You do not have permission to create invoices.")
        invoice = InvoiceService.create(
            organization=organization,
            patient=patient,
            data=self._request.data,
            items=self._request.items,
            performed_by=actor,
        )
        event = BillingInvoiceCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            invoice_id=invoice.pk,
            patient_id=invoice.patient_id,
            organization_id=invoice.organization_id,
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=invoice,
            message="Invoice created successfully.",
            code="billing_invoice_created",
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class InvoiceMutationRequest:
    """Input required for an invoice mutation."""

    organization_id: UUID
    invoice_id: UUID
    data: dict[str, Any] | None = None


class InvoiceUpdateWorkflow(BaseWorkflow):
    """Update invoices through policy and service boundaries."""

    workflow_name = "billing.invoice.update"

    def __init__(self, *, request: InvoiceMutationRequest, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or BillingPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Update an invoice and publish its event after commit."""
        actor, organization = _resolve(context, self._request.organization_id)
        try:
            invoice = Invoice.objects.get(
                pk=self._request.invoice_id,
                organization_id=organization.pk,
            )
        except Invoice.DoesNotExist as exc:
            raise BillingNotFoundError("Invoice was not found.") from exc
        if not self._policy.can_update_invoice(actor=actor, organization=organization):
            raise PermissionError("You do not have permission to update invoices.")
        updated = InvoiceService.update(
            invoice=invoice,
            data=self._request.data or {},
            performed_by=actor,
        )
        event = BillingInvoiceCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            invoice_id=updated.pk,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Invoice updated successfully.",
            code="billing_invoice_updated",
        )


class InvoiceVoidWorkflow(BaseWorkflow):
    """Void an invoice through policy and service boundaries."""

    workflow_name = "billing.invoice.void"

    def __init__(self, *, request: InvoiceMutationRequest, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or BillingPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Void an invoice."""
        actor, organization = _resolve(context, self._request.organization_id)
        invoice = Invoice.objects.get(
            pk=self._request.invoice_id, organization_id=organization.pk
        )
        if not self._policy.can_void_invoice(actor=actor, organization=organization):
            raise PermissionError("You do not have permission to void invoices.")
        updated = InvoiceService.void(invoice=invoice, performed_by=actor)
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Invoice voided successfully.",
            code="billing_invoice_voided",
        )


class InvoiceDeleteWorkflow(BaseWorkflow):
    """Soft-delete an invoice through policy and service boundaries."""

    workflow_name = "billing.invoice.delete"

    def __init__(self, *, request: InvoiceMutationRequest, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or BillingPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Soft-delete an invoice."""
        actor, organization = _resolve(context, self._request.organization_id)
        invoice = Invoice.objects.get(
            pk=self._request.invoice_id, organization_id=organization.pk
        )
        if not self._policy.can_delete_invoice(actor=actor, organization=organization):
            raise PermissionError("You do not have permission to delete invoices.")
        updated = InvoiceService.delete(invoice=invoice, performed_by=actor)
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Invoice deleted successfully.",
            code="billing_invoice_deleted",
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class PaymentCreationRequest:
    """Input required for payment creation."""

    organization_id: UUID
    patient_id: UUID
    data: dict[str, Any]


class PaymentCreationWorkflow(BaseWorkflow):
    """Create payments through policy and service boundaries."""

    workflow_name = "billing.payment.create"

    def __init__(self, *, request: PaymentCreationRequest, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or BillingPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Create a payment and publish its event after commit."""
        actor, organization = _resolve(context, self._request.organization_id)
        patient = _patient(organization, self._request.patient_id)
        if not self._policy.can_process_payment(actor=actor, organization=organization):
            raise PermissionError("You do not have permission to process payments.")
        payment = PaymentService.create(
            organization=organization,
            patient=patient,
            data=self._request.data,
            performed_by=actor,
        )
        event = BillingPaymentCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            payment_id=payment.pk,
            invoice_id=payment.invoice_id,
            patient_id=payment.patient_id,
            organization_id=payment.organization_id,
            amount=payment.amount,
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=payment,
            message="Payment recorded successfully.",
            code="billing_payment_created",
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ClaimCreationRequest:
    """Input required for claim submission."""

    organization_id: UUID
    patient_id: UUID
    invoice_id: UUID
    data: dict[str, Any]


class ClaimCreationWorkflow(BaseWorkflow):
    """Submit claims through policy and service boundaries."""

    workflow_name = "billing.claim.create"

    def __init__(self, *, request: ClaimCreationRequest, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or BillingPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Submit a claim and publish its event after commit."""
        actor, organization = _resolve(context, self._request.organization_id)
        patient = _patient(organization, self._request.patient_id)
        invoice = Invoice.objects.get(
            pk=self._request.invoice_id, organization_id=organization.pk
        )
        if not self._policy.can_submit_claim(actor=actor, organization=organization):
            raise PermissionError("You do not have permission to submit claims.")
        claim = InsuranceClaimService.create(
            organization=organization,
            patient=patient,
            invoice=invoice,
            data=self._request.data,
            performed_by=actor,
        )
        event = BillingInvoiceCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            invoice_id=claim.invoice_id,
            patient_id=claim.patient_id,
            organization_id=claim.organization_id,
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=claim,
            message="Insurance claim submitted successfully.",
            code="billing_claim_created",
        )


@dataclass(frozen=True, slots=True, kw_only=True)
class ClaimTransitionRequest:
    """Input required for a claim transition."""

    organization_id: UUID
    claim_id: UUID


class ClaimApprovalWorkflow(BaseWorkflow):
    """Approve claims through policy and service boundaries."""

    workflow_name = "billing.claim.approve"

    def __init__(
        self,
        *,
        request: ClaimTransitionRequest,
        approved_amount: Decimal,
        policy=None,
        logger_=None,
    ):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._approved_amount = approved_amount
        self._policy = policy or BillingPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Approve a claim and publish its status event."""
        actor, organization = _resolve(context, self._request.organization_id)
        claim = _claim(organization, self._request.claim_id)
        if not self._policy.can_approve_claim(actor=actor, organization=organization):
            raise PermissionError("You do not have permission to approve claims.")
        previous = claim.status
        updated = InsuranceClaimService.approve(
            claim=claim, approved_amount=self._approved_amount, performed_by=actor
        )
        self.publish_after_commit(
            BillingClaimStatusChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                claim_id=updated.pk,
                invoice_id=updated.invoice_id,
                patient_id=updated.patient_id,
                organization_id=updated.organization_id,
                previous_status=previous,
                status=updated.status,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Insurance claim approved successfully.",
            code="billing_claim_approved",
        )


class ClaimRejectWorkflow(BaseWorkflow):
    """Reject claims through policy and service boundaries."""

    workflow_name = "billing.claim.reject"

    def __init__(
        self,
        *,
        request: ClaimTransitionRequest,
        rejection_reason: str,
        policy=None,
        logger_=None,
    ):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._reason = rejection_reason
        self._policy = policy or BillingPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Reject a claim and publish its status event."""
        actor, organization = _resolve(context, self._request.organization_id)
        claim = _claim(organization, self._request.claim_id)
        if not self._policy.can_approve_claim(actor=actor, organization=organization):
            raise PermissionError("You do not have permission to reject claims.")
        previous = claim.status
        updated = InsuranceClaimService.reject(
            claim=claim, rejection_reason=self._reason, performed_by=actor
        )
        self.publish_after_commit(
            BillingClaimStatusChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                claim_id=updated.pk,
                invoice_id=updated.invoice_id,
                patient_id=updated.patient_id,
                organization_id=updated.organization_id,
                previous_status=previous,
                status=updated.status,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Insurance claim rejected successfully.",
            code="billing_claim_rejected",
        )


class ClaimAppealWorkflow(BaseWorkflow):
    """Appeal rejected claims through policy and service boundaries."""

    workflow_name = "billing.claim.appeal"

    def __init__(self, *, request: ClaimTransitionRequest, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or BillingPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Appeal a claim and publish its status event."""
        actor, organization = _resolve(context, self._request.organization_id)
        claim = _claim(organization, self._request.claim_id)
        if not self._policy.can_approve_claim(actor=actor, organization=organization):
            raise PermissionError("You do not have permission to appeal claims.")
        previous = claim.status
        updated = InsuranceClaimService.appeal(claim=claim, performed_by=actor)
        self.publish_after_commit(
            BillingClaimStatusChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                claim_id=updated.pk,
                invoice_id=updated.invoice_id,
                patient_id=updated.patient_id,
                organization_id=updated.organization_id,
                previous_status=previous,
                status=updated.status,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Insurance claim appealed successfully.",
            code="billing_claim_appealed",
        )


class ClaimSettleWorkflow(BaseWorkflow):
    """Settle approved claims through policy and service boundaries."""

    workflow_name = "billing.claim.settle"

    def __init__(self, *, request: ClaimTransitionRequest, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or BillingPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Settle a claim and publish its status event."""
        actor, organization = _resolve(context, self._request.organization_id)
        claim = _claim(organization, self._request.claim_id)
        if not self._policy.can_settle_claim(actor=actor, organization=organization):
            raise PermissionError("You do not have permission to settle claims.")
        previous = claim.status
        updated = InsuranceClaimService.settle(claim=claim, performed_by=actor)
        self.publish_after_commit(
            BillingClaimStatusChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                claim_id=updated.pk,
                invoice_id=updated.invoice_id,
                patient_id=updated.patient_id,
                organization_id=updated.organization_id,
                previous_status=previous,
                status=updated.status,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Insurance claim settled successfully.",
            code="billing_claim_settled",
        )


__all__ = (
    "ClaimAppealWorkflow",
    "ClaimApprovalRequest",
    "ClaimApprovalWorkflow",
    "ClaimCreationRequest",
    "ClaimCreationWorkflow",
    "ClaimRejectWorkflow",
    "ClaimSettleWorkflow",
    "ClaimTransitionRequest",
    "InvoiceCreationRequest",
    "InvoiceCreationWorkflow",
    "InvoiceDeleteWorkflow",
    "InvoiceMutationRequest",
    "InvoiceUpdateWorkflow",
    "InvoiceVoidWorkflow",
    "PaymentCreationRequest",
    "PaymentCreationWorkflow",
)
