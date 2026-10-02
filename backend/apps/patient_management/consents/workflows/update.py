"""
Patient Consent update workflow.
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
from apps.patient_management.consents.events import (
    PatientConsentUpdatedEvent,
)
from apps.patient_management.consents.models import (
    PatientConsent,
)
from apps.patient_management.consents.policies import (
    PatientConsentPolicy,
)
from apps.patient_management.consents.services import (
    update_consent,
)
from apps.platform.accounts.models import (
    User,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientConsentUpdateRequest:
    """
    Input required to update a Patient Consent.
    """

    consent_id: UUID
    data: dict[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientConsentUpdateData:
    """
    Result returned after Patient Consent update.
    """

    consent_id: UUID
    patient_id: UUID
    organization_id: UUID
    updated: bool
    event_id: UUID | None = None


class PatientConsentUpdateWorkflow(
    BaseWorkflow[PatientConsentUpdateData],
):
    """
    Update a Patient Consent within the current tenant.
    """

    workflow_name = "consent.update"

    def __init__(
        self,
        *,
        request: PatientConsentUpdateRequest,
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
    ) -> WorkflowResult[PatientConsentUpdateData]:
        """
        Execute the Patient Consent update workflow.
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

        if not self._policy.can_update(
            actor=actor,
            consent=consent,
        ):
            raise PermissionError(
                "You do not have permission to update this patient consent.",
            )

        changes = dict(
            self._request.data,
        )

        if not changes:
            return WorkflowResult.ok(
                context=context,
                data=PatientConsentUpdateData(
                    consent_id=consent.pk,
                    patient_id=consent.patient_id,
                    organization_id=consent.organization_id,
                    updated=False,
                ),
                message="No consent changes were supplied.",
                code="consent_unchanged",
            )

        updated = update_consent(
            instance=consent,
            validated_data=changes,
            performed_by=actor,
        )

        event = PatientConsentUpdatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            consent_id=updated.pk,
            patient_id=updated.patient_id,
            organization_id=updated.organization_id,
            changes=changes,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientConsentUpdateData(
                consent_id=updated.pk,
                patient_id=updated.patient_id,
                organization_id=updated.organization_id,
                updated=True,
                event_id=event.event_id,
            ),
            message="Patient consent updated successfully.",
            code="consent_updated",
        )


__all__ = (
    "PatientConsentUpdateData",
    "PatientConsentUpdateRequest",
    "PatientConsentUpdateWorkflow",
)
