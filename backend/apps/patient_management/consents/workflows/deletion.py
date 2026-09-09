"""
Patient Consent deletion workflow.
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
from apps.patient_management.consents.events import (
    PatientConsentDeletedEvent,
)
from apps.patient_management.consents.models import (
    PatientConsent,
)
from apps.patient_management.consents.policies import (
    PatientConsentPolicy,
)
from apps.patient_management.consents.services import (
    delete_consent,
)
from apps.platform.accounts.models import (
    User,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientConsentDeletionRequest:
    """
    Input required to delete a Patient Consent.
    """

    consent_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientConsentDeletionData:
    """
    Result returned after Patient Consent deletion.
    """

    consent_id: UUID
    patient_id: UUID
    organization_id: UUID
    deleted: bool
    event_id: UUID | None = None


class PatientConsentDeletionWorkflow(
    BaseWorkflow[PatientConsentDeletionData],
):
    """
    Soft-delete a Patient Consent within the current tenant.
    """

    workflow_name = "consent.delete"

    def __init__(
        self,
        *,
        request: PatientConsentDeletionRequest,
        policy: PatientConsentPolicy | None = None,
        logger_=None,
    ) -> None:
        """Initialize the workflow instance."""
        super().__init__(
            logger_=logger_,
            payload=request,
        )
        self._request = request
        self._policy = policy or PatientConsentPolicy()

    @transaction.atomic
    def _run(
        self,
        context: WorkflowContext,
    ) -> WorkflowResult[PatientConsentDeletionData]:
        """
        Execute the Patient Consent deletion workflow.
        """
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            consent = PatientConsent.objects.select_related(
                "organization",
                "patient",
            ).get(
                pk=self._request.consent_id,
                organization__tenant_id=context.tenant_id,
                is_deleted=False,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient consent was not found.",
            ) from exc

        if not self._policy.can_delete(
            actor=actor,
            consent=consent,
        ):
            raise PermissionError(
                "You do not have permission to delete this patient consent.",
            )

        delete_consent(
            instance=consent,
            performed_by=actor,
        )

        event = PatientConsentDeletedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            consent_id=consent.pk,
            patient_id=consent.patient_id,
            organization_id=consent.organization_id,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientConsentDeletionData(
                consent_id=consent.pk,
                patient_id=consent.patient_id,
                organization_id=consent.organization_id,
                deleted=True,
                event_id=event.event_id,
            ),
            message="Patient consent deleted successfully.",
            code="consent_deleted",
        )


__all__ = (
    "PatientConsentDeletionData",
    "PatientConsentDeletionRequest",
    "PatientConsentDeletionWorkflow",
)
