"""
Workflow for updating a Patient Relationship.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import (
    BaseWorkflow,
    WorkflowContext,
    WorkflowResult,
)
from apps.patient_management.relationships.events import (
    PatientRelationshipUpdatedEvent,
)
from apps.patient_management.relationships.models import PatientRelationship
from apps.patient_management.relationships.policies import (
    PatientRelationshipPolicy,
)
from apps.patient_management.relationships.services import (
    update_patient_relationship,
)
from apps.platform.accounts.models import User


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipUpdateRequest:
    """
    Input required to update a Patient Relationship.
    """

    relationship_id: UUID
    data: dict[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipUpdateData:
    """
    Result returned after successful update.
    """

    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
    updated: bool
    event_id: UUID


class PatientRelationshipUpdateWorkflow(
    BaseWorkflow[PatientRelationshipUpdateData],
):
    """
    Update a tenant-scoped Patient Relationship.
    """

    workflow_name = "relationship.update"

    def __init__(
        self,
        *,
        request: PatientRelationshipUpdateRequest,
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
    ) -> WorkflowResult[PatientRelationshipUpdateData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            relationship = PatientRelationship.objects.select_related(
                "organization",
                "patient",
                "related_patient",
            ).get(
                pk=self._request.relationship_id,
                organization__tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient relationship was not found.",
            ) from exc

        if not self._policy.can_update(
            actor=actor,
            relationship=relationship,
        ):
            raise PermissionError(
                "You do not have permission to update this patient relationship.",
            )

        changes = dict(
            self._request.data,
        )

        relationship = update_patient_relationship(
            instance=relationship,
            validated_data=changes,
            performed_by=actor,
        )

        event = PatientRelationshipUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            changes=changes,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipUpdateData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient relationship updated successfully.",
            code="relationship_updated",
        )


__all__ = (
    "PatientRelationshipUpdateData",
    "PatientRelationshipUpdateRequest",
    "PatientRelationshipUpdateWorkflow",
)
