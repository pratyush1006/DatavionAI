"""
Patient Identifier creation workflow.
"""

from __future__ import annotations

from collections.abc import Mapping
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
from apps.patient_management.identifiers.events import (
    IdentifierCreatedEvent,
)
from apps.patient_management.identifiers.policies import IdentifierPolicy
from apps.patient_management.identifiers.services import (
    create_patient_identifier,
)
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierCreationRequest:
    """Patient Identifier creation request."""

    organization_id: UUID
    patient_id: UUID
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierCreationData:
    """Patient Identifier creation result."""

    identifier_id: UUID
    created: bool
    event_id: UUID | None = None


class IdentifierCreationWorkflow(
    BaseWorkflow[IdentifierCreationData],
):
    """Create a patient identifier inside the current tenant."""

    def __init__(
        self,
        *,
        request: IdentifierCreationRequest,
        policy: IdentifierPolicy | None = None,
    ) -> None:
        super().__init__()
        self._request = request
        self._policy = policy or IdentifierPolicy()

    @transaction.atomic
    def _run(
        self,
        *,
        context: WorkflowContext,
    ) -> WorkflowResult[IdentifierCreationData]:
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
                "User does not have permission to create identifier.",
            )

        data = dict(self._request.data)
        data["organization"] = organization
        data["patient"] = patient

        identifier = create_patient_identifier(
            validated_data=data,
            performed_by=actor,
        )

        event = IdentifierCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            identifier_id=identifier.id,
            patient_id=identifier.patient_id,
            organization_id=identifier.organization_id,
            identifier_type=identifier.identifier_type,
            status=identifier.status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=IdentifierCreationData(
                identifier_id=identifier.id,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient identifier created successfully.",
            code="identifier_created",
        )


__all__ = (
    "IdentifierCreationData",
    "IdentifierCreationRequest",
    "IdentifierCreationWorkflow",
)
