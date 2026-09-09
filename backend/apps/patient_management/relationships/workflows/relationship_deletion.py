"""
Workflow for deleting a Patient Relationship.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.relationships.events import (
    PatientRelationshipDeletedEvent,
)
from apps.patient_management.relationships.models import PatientRelationship
from apps.patient_management.relationships.policies import (
    PatientRelationshipPolicy,
)
from apps.patient_management.relationships.services import (
    delete_patient_relationship,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipDeletionRequest:
    """
    Input required to delete a Patient Relationship.
    """

    relationship_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipDeletionData:
    """
    Result returned after successful deletion.
    """

    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
    deleted: bool
    event_id: UUID


class PatientRelationshipDeletionWorkflow(
    BaseWorkflow[PatientRelationshipDeletionData],
):
    """
    Delete a tenant-scoped Patient Relationship.
    """

    workflow_name = "relationship.delete"

    def __init__(
        self,
        *,
        request: PatientRelationshipDeletionRequest,
        policy: PatientRelationshipPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientRelationshipPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientRelationshipDeletionData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            relationship = PatientRelationship.objects.select_related(
                "organization",
                "patient",
            ).get(
                pk=self._request.relationship_id,
                organization__tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient relationship was not found.",
            ) from exc

        if not self._policy.can_delete(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to delete this patient relationship.",
            )

        relationship_id = relationship.pk
        patient_id = relationship.patient_id
        organization_id = relationship.organization_id

        delete_patient_relationship(
            instance=relationship,
            performed_by=actor,
        )

        event = PatientRelationshipDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship_id,
            patient_id=patient_id,
            organization_id=organization_id,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipDeletionData(
                relationship_id=relationship_id,
                patient_id=patient_id,
                organization_id=organization_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Patient relationship deleted successfully.",
            code="relationship_deleted",
        )


__all__ = (
    "PatientRelationshipDeletionData",
    "PatientRelationshipDeletionRequest",
    "PatientRelationshipDeletionWorkflow",
)
