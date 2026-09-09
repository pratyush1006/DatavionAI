"""
Workflow for deactivating a patient identifier.
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
    IdentifierStatusChangedEvent,
)
from apps.patient_management.identifiers.models import PatientIdentifier
from apps.patient_management.identifiers.policies import IdentifierPolicy
from apps.patient_management.identifiers.services import (
    deactivate_patient_identifier,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierDeactivationRequest:
    """Input required to deactivate a patient identifier."""

    identifier_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierDeactivationResult:
    """Successful patient identifier deactivation payload."""

    identifier_id: UUID
    status: str
    deactivated: bool
    event_id: UUID


class IdentifierDeactivationWorkflow(
    BaseWorkflow[IdentifierDeactivationResult],
):
    """Deactivate a patient identifier within the current tenant."""

    workflow_name = "identifier.deactivate"

    def __init__(
        self,
        *,
        request: IdentifierDeactivationRequest,
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
    ) -> WorkflowResult[IdentifierDeactivationResult]:
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

            if not self._policy.can_deactivate(
                actor=actor,
                identifier=identifier,
            ):
                raise PermissionError(
                    "You do not have permission to deactivate this identifier."
                )

            previous_status = identifier.status

            identifier = deactivate_patient_identifier(
                instance=identifier,
                performed_by=actor,
            )

            event = IdentifierStatusChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                identifier_id=identifier.pk,
                patient_id=identifier.patient_id,
                organization_id=organization.pk,
                previous_status=previous_status,
                new_status=identifier.status,
            )

            self.publish_after_commit(event)

            result = IdentifierDeactivationResult(
                identifier_id=identifier.pk,
                status=identifier.status,
                deactivated=True,
                event_id=event.event_id,
            )

            return WorkflowResult.ok(
                context=context,
                data=result,
                message="Patient identifier deactivated successfully.",
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient identifier was not found.",
            ) from exc


__all__ = (
    "IdentifierDeactivationRequest",
    "IdentifierDeactivationResult",
    "IdentifierDeactivationWorkflow",
)
