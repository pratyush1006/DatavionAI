"""
Workflow for setting a patient identifier as primary.
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
    IdentifierPrimaryChangedEvent,
)
from apps.patient_management.identifiers.models import PatientIdentifier
from apps.patient_management.identifiers.policies import IdentifierPolicy
from apps.patient_management.identifiers.services import (
    set_primary_patient_identifier,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierPrimaryRequest:
    """Input required to make an identifier primary."""

    identifier_id: UUID


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierPrimaryResult:
    """Successful primary identifier change payload."""

    identifier_id: UUID
    patient_id: UUID
    identifier_type: str
    is_primary: bool
    event_id: UUID


class IdentifierPrimaryWorkflow(
    BaseWorkflow[IdentifierPrimaryResult],
):
    """Set a patient identifier as the primary identifier."""

    workflow_name = "identifier.set_primary"

    def __init__(
        self,
        *,
        request: IdentifierPrimaryRequest,
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
    ) -> WorkflowResult[IdentifierPrimaryResult]:
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

            if not self._policy.can_set_primary(
                actor=actor,
                identifier=identifier,
            ):
                raise PermissionError(
                    "You do not have permission to set this identifier as primary."
                )

            previous_primary = identifier.is_primary

            identifier = set_primary_patient_identifier(
                instance=identifier,
                performed_by=actor,
            )

            event = IdentifierPrimaryChangedEvent(
                tenant_id=context.tenant_id,
                actor_id=actor.pk,
                identifier_id=identifier.pk,
                patient_id=identifier.patient_id,
                organization_id=organization.pk,
                identifier_type=identifier.identifier_type,
                previous_primary=previous_primary,
                new_primary=identifier.is_primary,
            )

            self.publish_after_commit(event)

            result = IdentifierPrimaryResult(
                identifier_id=identifier.pk,
                patient_id=identifier.patient_id,
                identifier_type=identifier.identifier_type,
                is_primary=identifier.is_primary,
                event_id=event.event_id,
            )

            return WorkflowResult.ok(
                context=context,
                data=result,
                message="Patient identifier set as primary successfully.",
            )

        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient identifier was not found.",
            ) from exc


__all__ = (
    "IdentifierPrimaryRequest",
    "IdentifierPrimaryResult",
    "IdentifierPrimaryWorkflow",
)
