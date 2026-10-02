"""
Workflow for creating a Patient Relationship.
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
from apps.patient_management.patients.models import Patient
from apps.patient_management.relationships.events import (
    PatientRelationshipCreatedEvent,
)
from apps.patient_management.relationships.policies import (
    PatientRelationshipPolicy,
)
from apps.patient_management.relationships.services import (
    create_patient_relationship,
)
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipCreationRequest:
    """
    Input required to create a Patient Relationship.
    """

    organization_id: UUID
    patient_id: UUID
    data: dict[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientRelationshipCreationData:
    """
    Result returned after successful creation.
    """

    relationship_id: UUID
    patient_id: UUID
    organization_id: UUID
    created: bool
    event_id: UUID


class PatientRelationshipCreationWorkflow(
    BaseWorkflow[PatientRelationshipCreationData],
):
    """
    Create a tenant-scoped Patient Relationship.
    """

    workflow_name = "relationship.create"

    def __init__(
        self,
        *,
        request: PatientRelationshipCreationRequest,
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
    ) -> WorkflowResult[PatientRelationshipCreationData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            organization = Organization.objects.get(
                pk=self._request.organization_id,
                tenant_id=context.tenant_id,
            )

            patient = Patient.objects.get(
                pk=self._request.patient_id,
                organization_id=organization.pk,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested organization or patient was not found.",
            ) from exc

        if not self._policy.can_create(
            actor=actor,
            organization=organization,
        ):
            raise PermissionError(
                "You do not have permission to create a patient relationship.",
            )

        validated_data = dict(
            self._request.data,
        )

        validated_data["organization"] = organization
        validated_data["patient"] = patient

        relationship = create_patient_relationship(
            validated_data=validated_data,
            performed_by=actor,
        )

        event = PatientRelationshipCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            relationship_id=relationship.pk,
            patient_id=relationship.patient_id,
            organization_id=relationship.organization_id,
            related_patient_id=relationship.related_patient_id,
            relationship_type=relationship.relationship_type,
            status=relationship.status,
            is_primary=relationship.is_primary,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientRelationshipCreationData(
                relationship_id=relationship.pk,
                patient_id=relationship.patient_id,
                organization_id=relationship.organization_id,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient relationship created successfully.",
            code="relationship_created",
        )


__all__ = (
    "PatientRelationshipCreationData",
    "PatientRelationshipCreationRequest",
    "PatientRelationshipCreationWorkflow",
)
