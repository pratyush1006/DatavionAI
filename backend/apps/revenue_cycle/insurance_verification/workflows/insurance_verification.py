"""Insurance Verification workflow orchestration."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any
from uuid import UUID

from apps.core.events import publish_after_commit
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.revenue_cycle.insurance_verification.events import (
    InsuranceVerificationCreatedEvent,
    InsuranceVerificationDeletedEvent,
    InsuranceVerificationRestoredEvent,
    InsuranceVerificationStatusChangedEvent,
    InsuranceVerificationUpdatedEvent,
)
from apps.revenue_cycle.insurance_verification.services import (
    InsuranceVerificationService,
)


@dataclass(frozen=True)
class InsuranceVerificationCreateRequest:
    """Input for Insurance Verification creation."""

    organization_id: UUID
    patient_id: UUID
    payer_id: str
    member_id: str
    request_reference: str
    idempotency_key: str
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class InsuranceVerificationUpdateRequest:
    """Input for Insurance Verification updates."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID
    data: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class InsuranceVerificationDeleteRequest:
    """Input for Insurance Verification deletion."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID
    deleted_by_id: UUID | None


@dataclass(frozen=True)
class InsuranceVerificationRestoreRequest:
    """Input for Insurance Verification restoration."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID


@dataclass(frozen=True)
class InsuranceVerificationLifecycleRequest:
    """Input for Insurance Verification lifecycle changes."""

    organization_id: UUID
    tenant_id: UUID
    verification_id: UUID
    target_status: str
    actor_id: UUID | None
    outcome: str | None = None
    response_code: str | None = None
    response_message: str | None = None
    response_payload: dict[str, Any] | None = None
    failure_reason: str | None = None


class InsuranceVerificationCreationWorkflow(BaseWorkflow):
    """Create an Insurance Verification and publish its event after commit."""

    def __init__(self, *, request: InsuranceVerificationCreateRequest, logger_=None):
        """Initialize the creation workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute creation."""

        request = self.payload
        verification = InsuranceVerificationService.create(
            organization_id=request.organization_id,
            patient_id=request.patient_id,
            request_reference=request.request_reference,
            idempotency_key=request.idempotency_key,
            payer_id=request.payer_id,
            member_id=request.member_id,
            data=request.data,
        )
        publish_after_commit(
            InsuranceVerificationCreatedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"request_reference": verification.request_reference},
            )
        )
        return WorkflowResult.ok(context=context, data=verification)


class InsuranceVerificationUpdateWorkflow(BaseWorkflow):
    """Update an Insurance Verification and publish its event after commit."""

    def __init__(self, *, request: InsuranceVerificationUpdateRequest, logger_=None):
        """Initialize the update workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute update."""

        request = self.payload
        verification = InsuranceVerificationService.update(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
            data=request.data,
        )
        publish_after_commit(
            InsuranceVerificationUpdatedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"updated": tuple(request.data)},
            )
        )
        return WorkflowResult.ok(context=context, data=verification)


class InsuranceVerificationDeletionWorkflow(BaseWorkflow):
    """Soft-delete an Insurance Verification and publish its event after commit."""

    def __init__(self, *, request: InsuranceVerificationDeleteRequest, logger_=None):
        """Initialize the deletion workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute deletion."""

        request = self.payload
        verification = InsuranceVerificationService.soft_delete(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
            deleted_by_id=request.deleted_by_id,
        )
        publish_after_commit(
            InsuranceVerificationDeletedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"deleted": True},
            )
        )
        return WorkflowResult.ok(context=context, data=verification)


class InsuranceVerificationRestoreWorkflow(BaseWorkflow):
    """Restore an Insurance Verification and publish its event after commit."""

    def __init__(self, *, request: InsuranceVerificationRestoreRequest, logger_=None):
        """Initialize the restoration workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute restoration."""

        request = self.payload
        verification = InsuranceVerificationService.restore(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
        )
        publish_after_commit(
            InsuranceVerificationRestoredEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"restored": True},
            )
        )
        return WorkflowResult.ok(context=context, data=verification)


class InsuranceVerificationLifecycleWorkflow(BaseWorkflow):
    """Transition an Insurance Verification and publish its event after commit."""

    def __init__(self, *, request: InsuranceVerificationLifecycleRequest, logger_=None):
        """Initialize the lifecycle workflow."""

        super().__init__(logger_=logger_, payload=request)

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Execute lifecycle transition."""

        request = self.payload
        verification = InsuranceVerificationService.transition(
            tenant_id=request.tenant_id,
            organization_id=request.organization_id,
            verification_id=request.verification_id,
            target_status=request.target_status,
            actor_id=request.actor_id,
            outcome=request.outcome,
            response_code=request.response_code,
            response_message=request.response_message,
            response_payload=request.response_payload,
            failure_reason=request.failure_reason,
        )
        publish_after_commit(
            InsuranceVerificationStatusChangedEvent(
                verification_id=verification.id,
                organization_id=verification.organization_id,
                patient_id=verification.patient_id,
                status=verification.status,
                payload={"outcome": verification.outcome},
            )
        )
        return WorkflowResult.ok(context=context, data=verification)


__all__ = (
    "InsuranceVerificationCreateRequest",
    "InsuranceVerificationCreationWorkflow",
    "InsuranceVerificationDeleteRequest",
    "InsuranceVerificationDeletionWorkflow",
    "InsuranceVerificationLifecycleRequest",
    "InsuranceVerificationLifecycleWorkflow",
    "InsuranceVerificationRestoreRequest",
    "InsuranceVerificationRestoreWorkflow",
    "InsuranceVerificationUpdateRequest",
    "InsuranceVerificationUpdateWorkflow",
)
