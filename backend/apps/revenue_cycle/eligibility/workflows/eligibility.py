"""Revenue Cycle Eligibility workflows."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.revenue_cycle.eligibility.events import (
    EligibilityCreatedEvent,
    EligibilityDeletedEvent,
    EligibilityRestoredEvent,
    EligibilityStatusChangedEvent,
    EligibilityUpdatedEvent,
)
from apps.revenue_cycle.eligibility.policies import EligibilityPolicy
from apps.revenue_cycle.eligibility.selectors import (
    get_deleted_eligibility_for_update,
    get_eligibility_for_update,
)
from apps.revenue_cycle.eligibility.services import EligibilityService


@dataclass(frozen=True, slots=True, kw_only=True)
class EligibilityCreationRequest:
    """Creation workflow input."""

    organization_id: UUID
    patient_id: UUID
    data: dict


@dataclass(frozen=True, slots=True, kw_only=True)
class EligibilityUpdateRequest:
    """Update workflow input."""

    organization_id: UUID
    eligibility_id: UUID
    data: dict


@dataclass(frozen=True, slots=True, kw_only=True)
class EligibilityLifecycleRequest:
    """Lifecycle workflow input."""

    organization_id: UUID
    eligibility_id: UUID
    status: str


@dataclass(frozen=True, slots=True, kw_only=True)
class EligibilityDeleteRequest:
    """Deletion workflow input."""

    organization_id: UUID
    eligibility_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class EligibilityRestoreRequest:
    """Restoration workflow input."""

    organization_id: UUID
    eligibility_id: UUID


def _resolve(context, organization_id):
    """Resolve actor and organization within the active tenant."""
    try:
        return User.objects.get(pk=context.actor_id), Organization.objects.get(
            pk=organization_id, tenant_id=context.tenant_id
        )
    except ObjectDoesNotExist as exc:
        raise ValueError("The requested actor or organization was not found.") from exc


def _patient(context, organization, patient_id):
    """Resolve the canonical Patient within the exact scope."""
    try:
        return Patient.objects.get(
            pk=patient_id,
            organization_id=organization.pk,
            organization__tenant_id=context.tenant_id,
            is_deleted=False,
        )
    except ObjectDoesNotExist as exc:
        raise ValueError(
            "The requested patient was not found in the organization."
        ) from exc


def _result(context, data, message, code):
    """Build a successful workflow result."""
    return WorkflowResult.ok(context=context, data=data, message=message, code=code)


class EligibilityCreationWorkflow(BaseWorkflow):
    """Create Eligibility through policy and service boundaries."""

    workflow_name = "revenue_cycle.eligibility.create"

    def __init__(self, *, request, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or EligibilityPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Create and publish after commit."""
        actor, organization = _resolve(context, self.request.organization_id)
        patient = _patient(context, organization, self.request.patient_id)
        if not self.policy.can_create(actor=actor, organization=organization):
            raise PermissionError(
                "You do not have permission to create eligibility records."
            )
        obj = EligibilityService.create(
            patient=patient,
            organization=organization,
            performed_by=actor,
            **dict(self.request.data),
        )
        event = EligibilityCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            eligibility_id=obj.pk,
            patient_id=obj.patient_id,
            organization_id=obj.organization_id,
        )
        self.publish_after_commit(event)
        return _result(
            context,
            obj,
            "Eligibility request created successfully.",
            "revenue_cycle_eligibility_created",
        )


class EligibilityUpdateWorkflow(BaseWorkflow):
    """Update Eligibility under a row lock."""

    workflow_name = "revenue_cycle.eligibility.update"

    def __init__(self, *, request, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or EligibilityPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Update and publish after commit."""
        actor, organization = _resolve(context, self.request.organization_id)
        obj = get_eligibility_for_update(
            tenant_id=context.tenant_id,
            organization_id=organization.pk,
            eligibility_id=self.request.eligibility_id,
        )
        if not self.policy.can_update(actor=actor, eligibility=obj):
            raise PermissionError(
                "You do not have permission to update eligibility records."
            )
        obj = EligibilityService.update(
            eligibility=obj, performed_by=actor, **dict(self.request.data)
        )
        event = EligibilityUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            eligibility_id=obj.pk,
            patient_id=obj.patient_id,
            organization_id=obj.organization_id,
        )
        self.publish_after_commit(event)
        return _result(
            context,
            obj,
            "Eligibility request updated successfully.",
            "revenue_cycle_eligibility_updated",
        )


class EligibilityLifecycleWorkflow(BaseWorkflow):
    """Apply strict Eligibility lifecycle transitions."""

    workflow_name = "revenue_cycle.eligibility.lifecycle"

    def __init__(self, *, request, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or EligibilityPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Transition and publish after commit."""
        actor, organization = _resolve(context, self.request.organization_id)
        obj = get_eligibility_for_update(
            tenant_id=context.tenant_id,
            organization_id=organization.pk,
            eligibility_id=self.request.eligibility_id,
        )
        if not self.policy.can_transition(actor=actor, eligibility=obj):
            raise PermissionError(
                "You do not have permission to change eligibility lifecycle."
            )
        previous = obj.status
        obj = EligibilityService.transition(
            eligibility=obj, status=self.request.status, performed_by=actor
        )
        event = EligibilityStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            eligibility_id=obj.pk,
            patient_id=obj.patient_id,
            organization_id=obj.organization_id,
            previous_status=previous,
            status=obj.status,
        )
        self.publish_after_commit(event)
        return _result(
            context,
            obj,
            "Eligibility lifecycle changed successfully.",
            "revenue_cycle_eligibility_status_changed",
        )


class EligibilityDeletionWorkflow(BaseWorkflow):
    """Soft-delete Eligibility under a row lock."""

    workflow_name = "revenue_cycle.eligibility.delete"

    def __init__(self, *, request, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or EligibilityPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Delete and publish after commit."""
        actor, organization = _resolve(context, self.request.organization_id)
        obj = get_eligibility_for_update(
            tenant_id=context.tenant_id,
            organization_id=organization.pk,
            eligibility_id=self.request.eligibility_id,
        )
        if not self.policy.can_delete(actor=actor, eligibility=obj):
            raise PermissionError(
                "You do not have permission to delete eligibility records."
            )
        obj = EligibilityService.delete(eligibility=obj, performed_by=actor)
        event = EligibilityDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            eligibility_id=obj.pk,
            patient_id=obj.patient_id,
            organization_id=obj.organization_id,
        )
        self.publish_after_commit(event)
        return _result(
            context,
            obj,
            "Eligibility request deleted successfully.",
            "revenue_cycle_eligibility_deleted",
        )


class EligibilityRestoreWorkflow(BaseWorkflow):
    """Restore Eligibility under a row lock."""

    workflow_name = "revenue_cycle.eligibility.restore"

    def __init__(self, *, request, policy=None, logger_=None):
        """Initialize the workflow."""
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or EligibilityPolicy()

    @transaction.atomic
    def _run(self, context: WorkflowContext) -> WorkflowResult:
        """Restore and publish after commit."""
        actor, organization = _resolve(context, self.request.organization_id)
        obj = get_deleted_eligibility_for_update(
            tenant_id=context.tenant_id,
            organization_id=organization.pk,
            eligibility_id=self.request.eligibility_id,
        )
        if not self.policy.can_restore(actor=actor, organization=organization):
            raise PermissionError(
                "You do not have permission to restore eligibility records."
            )
        obj = EligibilityService.restore(eligibility=obj, performed_by=actor)
        event = EligibilityRestoredEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            eligibility_id=obj.pk,
            patient_id=obj.patient_id,
            organization_id=obj.organization_id,
        )
        self.publish_after_commit(event)
        return _result(
            context,
            obj,
            "Eligibility request restored successfully.",
            "revenue_cycle_eligibility_restored",
        )


__all__ = (
    "EligibilityCreationRequest",
    "EligibilityCreationWorkflow",
    "EligibilityDeleteRequest",
    "EligibilityDeletionWorkflow",
    "EligibilityLifecycleRequest",
    "EligibilityLifecycleWorkflow",
    "EligibilityRestoreRequest",
    "EligibilityRestoreWorkflow",
    "EligibilityUpdateRequest",
    "EligibilityUpdateWorkflow",
)
