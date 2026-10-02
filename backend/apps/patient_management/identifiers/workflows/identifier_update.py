"""
Patient Identifier update workflow.
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
    IdentifierUpdatedEvent,
)
from apps.patient_management.identifiers.models import PatientIdentifier
from apps.patient_management.identifiers.policies import IdentifierPolicy
from apps.patient_management.identifiers.services import (
    update_patient_identifier,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierUpdateRequest:
    """Patient Identifier update request."""

    identifier_id: UUID
    data: Mapping[str, Any]


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierUpdateData:
    """Patient Identifier update result."""

    identifier_id: UUID
    updated: bool
    event_id: UUID | None = None


class IdentifierUpdateWorkflow(
    BaseWorkflow[IdentifierUpdateData],
):
    """Update a tenant-scoped patient identifier."""

    def __init__(
        self,
        *,
        request: IdentifierUpdateRequest,
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
    ) -> WorkflowResult[IdentifierUpdateData]:
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )

            identifier = PatientIdentifier.objects.select_related(
                "organization",
                "patient",
            ).get(
                pk=self._request.identifier_id,
                organization__tenant_id=context.tenant_id,
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "The requested patient identifier was not found.",
            ) from exc

        if not self._policy.can_update(
            actor=actor,
            identifier=identifier,
        ):
            raise PermissionError(
                "User does not have permission to update identifier.",
            )

        data = dict(self._request.data)

        if not data:
            return WorkflowResult.ok(
                context=context,
                data=IdentifierUpdateData(
                    identifier_id=identifier.id,
                    updated=False,
                ),
                message="No identifier changes were supplied.",
                code="identifier_unchanged",
            )

        updated = update_patient_identifier(
            instance=identifier,
            validated_data=data,
            performed_by=actor,
        )

        event = IdentifierUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            identifier_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            identifier_type=updated.identifier_type,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=IdentifierUpdateData(
                identifier_id=updated.id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient identifier updated successfully.",
            code="identifier_updated",
        )


__all__ = (
    "IdentifierUpdateData",
    "IdentifierUpdateRequest",
    "IdentifierUpdateWorkflow",
)
