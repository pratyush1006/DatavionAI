"""
Patient Identifier verification workflow.
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
from apps.patient_management.identifiers.constants import VerificationStatus
from apps.patient_management.identifiers.events import (
    IdentifierVerifiedEvent,
)
from apps.patient_management.identifiers.models import PatientIdentifier
from apps.patient_management.identifiers.policies import IdentifierPolicy
from apps.patient_management.identifiers.services import (
    verify_patient_identifier,
)
from apps.platform.accounts.models import User


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierVerificationRequest:
    """Identifier verification request."""

    identifier_id: UUID
    status: VerificationStatus | str
    verification_source: str
    reference_number: str = ""
    remarks: str = ""


@dataclass(frozen=True, slots=True, kw_only=True)
class IdentifierVerificationData:
    """Identifier verification result."""

    identifier_id: UUID
    verification_status: str
    verified: bool
    event_id: UUID | None = None


class IdentifierVerificationWorkflow(
    BaseWorkflow[IdentifierVerificationData],
):
    """Record and apply a patient identifier verification decision."""

    def __init__(
        self,
        *,
        request: IdentifierVerificationRequest,
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
    ) -> WorkflowResult[IdentifierVerificationData]:
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

        if not self._policy.can_verify(
            actor=actor,
            identifier=identifier,
        ):
            raise PermissionError(
                "User does not have permission to verify identifier.",
            )

        previous_status = identifier.verification_status

        status = (
            self._request.status.value
            if isinstance(
                self._request.status,
                VerificationStatus,
            )
            else self._request.status
        )

        updated = verify_patient_identifier(
            instance=identifier,
            status=status,
            verification_source=self._request.verification_source,
            reference_number=self._request.reference_number,
            remarks=self._request.remarks,
            performed_by=actor,
        )

        event = IdentifierVerifiedEvent(
            tenant_id=context.tenant_id,
            actor_id=context.actor_id,
            identifier_id=updated.id,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            previous_status=previous_status,
            new_status=updated.verification_status,
        )

        self.publish_after_commit(event)

        return WorkflowResult.ok(
            context=context,
            data=IdentifierVerificationData(
                identifier_id=updated.id,
                verification_status=updated.verification_status,
                verified=(updated.verification_status == VerificationStatus.VERIFIED),
                event_id=event.event_id,
            ),
            message=("Patient identifier verification recorded successfully."),
            code="identifier_verified",
        )


__all__ = (
    "IdentifierVerificationData",
    "IdentifierVerificationRequest",
    "IdentifierVerificationWorkflow",
)
