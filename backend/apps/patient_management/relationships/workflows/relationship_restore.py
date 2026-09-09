"""Workflow for restoring a deleted Patient Relationship."""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowResult
from apps.patient_management.relationships.events import (
    PatientRelationshipStatusChangedEvent,
)
from apps.patient_management.relationships.models import PatientRelationship
from apps.patient_management.relationships.policies import PatientRelationshipPolicy
from apps.patient_management.relationships.services import (
    restore_patient_relationship,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientRelationshipRestoreRequest:
    relationship_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class PatientRelationshipRestoreData:
    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
    restored: bool
    event_id: UUID


class PatientRelationshipRestoreWorkflow(BaseWorkflow[PatientRelationshipRestoreData]):
    """Restore a soft-deleted Patient Relationship."""

    workflow_name = "relationship.restore"

    def __init__(self, *, request, policy=None, logger_=None) -> None:
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(self, context):
        try:
            actor = User.objects.get(pk=context.actor_id)
            relationship = PatientRelationship.deleted_objects.select_related(
                "organization",
                "patient",
                "related_patient",
            ).get(
                id=self._request.relationship_id,
                organization__tenant_id=context.tenant_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Deleted patient relationship was not found.") from exc

        if not self._policy.can_restore(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to restore this patient relationship."
            )

        previous_status = relationship.status

        relationship = restore_patient_relationship(
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
            data=PatientRelationshipRestoreData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                restored=True,
                event_id=event.event_id,
            ),
            message="Patient relationship restored successfully.",
            code="relationship_restored",
        )


__all__ = (
    "PatientRelationshipRestoreData",
    "PatientRelationshipRestoreRequest",
    "PatientRelationshipRestoreWorkflow",
)
