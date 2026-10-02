"""Workflow orchestration for Revenue Cycle Electronic Remittance Advice."""

from __future__ import annotations

from dataclasses import dataclass, field

from django.db import transaction

from apps.core.events import publish_after_commit
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult

from ..events import ERAEvent
from ..models import ERA
from ..services import delete_era, post_era, restore_era, reverse_era, validate_era


@dataclass(frozen=True)
class ERAWorkflowRequest:
    """Carry tenant, organization, actor, and ERA workflow input."""

    actor: object
    organization_id: object
    tenant_id: object
    era_id: object | None = None
    data: dict = field(default_factory=dict)


def _event(era: ERA, action: str) -> None:
    """Publish an ERA domain event after transaction commit."""
    publish_after_commit(
        ERAEvent(
            era_id=era.id,
            organization_id=era.organization_id,
            action=action,
        )
    )


class CreateERAWorkflow(BaseWorkflow):
    """Create an ERA aggregate."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Create the ERA inside an atomic transaction."""
        request = self.payload
        with transaction.atomic():
            era = ERA.objects.create(
                organization_id=request.organization_id,
                patient_id=request.data.get("patient_id"),
                payer_name=request.data["payer_name"],
                payer_identifier=request.data.get("payer_identifier", ""),
                trace_number=request.data["trace_number"],
                check_or_eft_number=request.data.get("check_or_eft_number", ""),
                source=request.data.get("source", "edi_835"),
                payment_amount=request.data.get("payment_amount", "0.00"),
                adjustment_amount=request.data.get("adjustment_amount", "0.00"),
                received_at=request.data["received_at"],
                external_reference=request.data.get("external_reference", ""),
                idempotency_key=request.data["idempotency_key"],
                raw_payload=request.data.get("raw_payload", {}),
                notes=request.data.get("notes", ""),
                processed_by=request.actor,
            )
            _event(era, "created")
        return WorkflowResult.ok(context=context, data=era)


class ValidateERAWorkflow(BaseWorkflow):
    """Validate an ERA aggregate."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Validate the ERA using a row lock."""
        request = self.payload
        with transaction.atomic():
            era = ERA.objects.select_for_update().get(pk=request.era_id)
            era = validate_era(era=era)
            _event(era, "validated")
        return WorkflowResult.ok(context=context, data=era)


class PostERAWorkflow(BaseWorkflow):
    """Post a validated ERA."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Post the ERA through the domain service."""
        request = self.payload
        with transaction.atomic():
            era = post_era(
                organization_id=request.organization_id,
                tenant_id=request.tenant_id,
                era_id=request.era_id,
                user=request.actor,
            )
            _event(era, "posted")
        return WorkflowResult.ok(context=context, data=era)


class ReverseERAWorkflow(BaseWorkflow):
    """Reverse a posted ERA."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Reverse the ERA through the domain service."""
        request = self.payload
        with transaction.atomic():
            era = reverse_era(
                organization_id=request.organization_id,
                tenant_id=request.tenant_id,
                era_id=request.era_id,
                user=request.actor,
            )
            _event(era, "reversed")
        return WorkflowResult.ok(context=context, data=era)


class DeleteERAWorkflow(BaseWorkflow):
    """Soft-delete an ERA."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Soft-delete the ERA through the domain service."""
        request = self.payload
        with transaction.atomic():
            era = delete_era(
                organization_id=request.organization_id,
                tenant_id=request.tenant_id,
                era_id=request.era_id,
                user_id=request.actor.id,
            )
            _event(era, "deleted")
        return WorkflowResult.ok(context=context, data=era)


class RestoreERAWorkflow(BaseWorkflow):
    """Restore a deleted ERA."""

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Restore the ERA through the domain service."""
        request = self.payload
        with transaction.atomic():
            era = restore_era(
                organization_id=request.organization_id,
                tenant_id=request.tenant_id,
                era_id=request.era_id,
            )
            _event(era, "restored")
        return WorkflowResult.ok(context=context, data=era)


__all__ = (
    "CreateERAWorkflow",
    "DeleteERAWorkflow",
    "ERAWorkflowRequest",
    "PostERAWorkflow",
    "RestoreERAWorkflow",
    "ReverseERAWorkflow",
    "ValidateERAWorkflow",
)
