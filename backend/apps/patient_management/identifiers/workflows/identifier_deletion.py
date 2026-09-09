"""
Workflow for deleting a patient identifier.
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
from apps.patient_management.identifiers.events import (
    IdentifierDeletedEvent,
)
from apps.patient_management.identifiers.models import PatientIdentifier
from apps.patient_management.identifiers.policies import IdentifierPolicy
from apps.patient_management.identifiers.services import (
    delete_patient_identifier,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierDeletionRequest:
    """Input required to delete a patient identifier."""

    identifier_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierDeletionResult:
    """Successful patient identifier deletion payload."""

    identifier_id: UUID
    deleted: bool
    event_id: UUID


class IdentifierDeletionWorkflow(
    BaseWorkflow[IdentifierDeletionResult],
):
    """Delete a patient identifier within the current tenant."""

    workflow_name = "identifier.delete"

    def __init__(
        self,
        *,
        request: IdentifierDeletionRequest,
        policy: IdentifierPolicy | None = None,
        logger_=None,
    ) -> None:
        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or IdentifierPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[IdentifierDeletionResult]:
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

            organization = identifier.organization

            if not self._policy.can_delete(
                actor=actor,
                identifier=identifier,
            ):
                raise PermissionError(
                    "You do not have permission to delete this identifier."
                )

            identifier_id = identifier.pk
            patient_id = identifier.patient_id
            identifier_type = identifier.identifier_type

            delete_patient_identifier(
                instance=identifier,
                performed_by=actor,
            )

            event = IdentifierDeletedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                identifier_id=identifier_id,
                patient_id=patient_id,
                organization_id=organization.pk,
                identifier_type=identifier_type,
            )

            self.publish_after_commit(event)

            result = IdentifierDeletionResult(
                identifier_id=identifier_id,
                deleted=True,
                event_id=event.event_id,
            )

            return WorkflowResult.ok(
                context=context,
                data=result,
                message="Patient identifier deleted successfully.",
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient identifier was not found.",
            ) from exc


__all__ = (
    "IdentifierDeletionRequest",
    "IdentifierDeletionResult",
    "IdentifierDeletionWorkflow",
)
