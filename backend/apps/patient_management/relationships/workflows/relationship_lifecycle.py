"""Lifecycle workflows for Patient Relationships."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.relationships.events import (
    PatientRelationshipPrimaryChangedEvent,
    PatientRelationshipStatusChangedEvent,
    PatientRelationshipTerminatedEvent,
    PatientRelationshipVerifiedEvent,
)
from apps.patient_management.relationships.policies import PatientRelationshipPolicy
from apps.patient_management.relationships.selectors import PatientRelationshipSelector
from apps.patient_management.relationships.services import (
    activate_patient_relationship,
    deactivate_patient_relationship,
    set_primary_patient_relationship,
    terminate_patient_relationship,
    verify_patient_relationship,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientRelationshipLifecycleRequest:
    relationship_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientRelationshipLifecycleData:
    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str
    verification_status: str
    is_primary: bool
    event_id: UUID


def _resolve_actor(context: WorkflowContext) -> User:
    try:
        return User.objects.get(pk=context.actor_id)
    except User.DoesNotExist as exc:
        raise ValueError("The acting user was not found.") from exc


def _resolve_relationship(
    *,
    request: PatientRelationshipLifecycleRequest,
    context: WorkflowContext,
):
    try:
        relationship = (
            PatientRelationshipSelector.queryset()
            .filter(
                id=request.relationship_id,
                organization__tenant_id=context.tenant_id,
            )
            .get()
        )
    except ObjectDoesNotExist as exc:
        raise ValueError("Patient relationship was not found.") from exc

    return relationship


def _resolve_organization(relationship):
    return Organization.objects.get(pk=relationship.organization_id)


class PatientRelationshipVerifyWorkflow(BaseWorkflow[PatientRelationshipLifecycleData]):
    workflow_name = "relationship.verify"

    def __init__(self, *, request, policy=None, logger_=None) -> None:
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(self, context):
        actor = _resolve_actor(context)
        relationship = _resolve_relationship(
            request=self._request,
            context=context,
        )
        if not self._policy.can_verify(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to verify this patient relationship."
            )

        relationship = verify_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipVerifiedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipLifecycleData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                previous_status=relationship.status,
                new_status=relationship.status,
                verification_status=relationship.verification_status,
                is_primary=relationship.is_primary,
                event_id=event.event_id,
            ),
            message="Patient relationship verified successfully.",
            code="relationship_verified",
        )


class PatientRelationshipTerminateWorkflow(
    BaseWorkflow[PatientRelationshipLifecycleData]
):
    workflow_name = "relationship.terminate"

    def __init__(self, *, request, policy=None, logger_=None) -> None:
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(self, context):
        actor = _resolve_actor(context)
        relationship = _resolve_relationship(
            request=self._request,
            context=context,
        )
        if not self._policy.can_terminate(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to terminate this patient relationship."
            )

        previous_status = relationship.status
        relationship = terminate_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipTerminatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            previous_status=previous_status,
            new_status=relationship.status,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipLifecycleData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                previous_status=previous_status,
                new_status=relationship.status,
                verification_status=relationship.verification_status,
                is_primary=relationship.is_primary,
                event_id=event.event_id,
            ),
            message="Patient relationship terminated successfully.",
            code="relationship_terminated",
        )


class PatientRelationshipSetPrimaryWorkflow(
    BaseWorkflow[PatientRelationshipLifecycleData]
):
    workflow_name = "relationship.set_primary"

    def __init__(self, *, request, policy=None, logger_=None) -> None:
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(self, context):
        actor = _resolve_actor(context)
        relationship = _resolve_relationship(
            request=self._request,
            context=context,
        )
        if not self._policy.can_set_primary(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to mark this patient relationship as primary."
            )

        relationship = set_primary_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipPrimaryChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            is_primary=relationship.is_primary,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipLifecycleData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                previous_status=relationship.status,
                new_status=relationship.status,
                verification_status=relationship.verification_status,
                is_primary=relationship.is_primary,
                event_id=event.event_id,
            ),
            message="Patient relationship marked as primary successfully.",
            code="relationship_primary_changed",
        )


class PatientRelationshipActivationWorkflow(
    BaseWorkflow[PatientRelationshipLifecycleData]
):
    workflow_name = "relationship.activate"

    def __init__(self, *, request, policy=None, logger_=None) -> None:
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(self, context):
        actor = _resolve_actor(context)
        relationship = _resolve_relationship(
            request=self._request,
            context=context,
        )
        if not self._policy.can_update(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to activate this patient relationship."
            )

        previous_status = relationship.status
        relationship = activate_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            previous_status=previous_status,
            new_status=relationship.status,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipLifecycleData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                previous_status=previous_status,
                new_status=relationship.status,
                verification_status=relationship.verification_status,
                is_primary=relationship.is_primary,
                event_id=event.event_id,
            ),
            message="Patient relationship activated successfully.",
            code="relationship_activated",
        )


class PatientRelationshipDeactivationWorkflow(
    BaseWorkflow[PatientRelationshipLifecycleData]
):
    workflow_name = "relationship.deactivate"

    def __init__(self, *, request, policy=None, logger_=None) -> None:
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(self, context):
        actor = _resolve_actor(context)
        relationship = _resolve_relationship(
            request=self._request,
            context=context,
        )
        if not self._policy.can_update(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to deactivate this patient relationship."
            )

        previous_status = relationship.status
        relationship = deactivate_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            previous_status=previous_status,
            new_status=relationship.status,
        )
        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipLifecycleData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                previous_status=previous_status,
                new_status=relationship.status,
                verification_status=relationship.verification_status,
                is_primary=relationship.is_primary,
                event_id=event.event_id,
            ),
            message="Patient relationship deactivated successfully.",
            code="relationship_deactivated",
        )


__all__ = (
    "PatientRelationshipActivationWorkflow",
    "PatientRelationshipDeactivationWorkflow",
    "PatientRelationshipLifecycleData",
    "PatientRelationshipLifecycleRequest",
    "PatientRelationshipSetPrimaryWorkflow",
    "PatientRelationshipTerminateWorkflow",
    "PatientRelationshipVerifyWorkflow",
)
