"""
Patient Consent lifecycle workflows.
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
    PatientConsentStatusChangedEvent,
)
from apps.patient_management.consents.models import (
    PatientConsent,
)
from apps.patient_management.consents.policies import (
    PatientConsentPolicy,
)
from apps.patient_management.consents.services import (
    grant_consent,
    restore_consent,
    revoke_consent,
)
from apps.platform.accounts.models import (
    User,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientConsentLifecycleRequest:
    """
    Input required for a Patient Consent lifecycle transition.
    """

    consent_id: UUID


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientConsentLifecycleData:
    """
    Result returned after a Patient Consent lifecycle transition.
    """

    consent_id: UUID
    patient_id: UUID
    organization_id: UUID
    previous_status: str
    new_status: str
    changed: bool
    event_id: UUID | None = None


def _load_consent(
    *,
    context: WorkflowContext,
    consent_id: UUID,
    deleted: bool = False,
):
    """
    Load one consent inside the current tenant.
    """
    return PatientConsent.objects.select_related(
        "organization",
        "patient",
    ).get(
        pk=consent_id,
        organization__tenant_id=context.tenant_id,
        is_deleted=deleted,
    )


class PatientConsentGrantWorkflow(
    BaseWorkflow[PatientConsentLifecycleData],
):
    """
    Grant a pending Patient Consent.
    """

    workflow_name = "consent.grant"

    def __init__(
        self,
        *,
        request: PatientConsentLifecycleRequest,
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
    ) -> WorkflowResult[PatientConsentLifecycleData]:
        """
        Execute the grant transition.
        """
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            consent = _load_consent(
                context=context,
                consent_id=self._request.consent_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient consent was not found.",
            ) from exc

        if not self._policy.can_grant(
            actor=actor,
            consent=consent,
        ):
            raise PermissionError(
                "You do not have permission to grant this patient consent.",
            )

        previous = consent.status
        consent = grant_consent(
            instance=consent,
            performed_by=actor,
        )

        event = PatientConsentStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            consent_id=consent.pk,
            patient_id=consent.patient_id,
            organization_id=consent.organization_id,
            previous_status=previous,
            new_status=consent.status,
        )
        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientConsentLifecycleData(
                consent_id=consent.pk,
                patient_id=consent.patient_id,
                organization_id=consent.organization_id,
                previous_status=previous,
                new_status=consent.status,
                changed=True,
                event_id=event.event_id,
            ),
            message="Patient consent granted successfully.",
            code="consent_granted",
        )


class PatientConsentRevokeWorkflow(
    BaseWorkflow[PatientConsentLifecycleData],
):
    """
    Revoke a granted Patient Consent.
    """

    workflow_name = "consent.revoke"

    def __init__(
        self,
        *,
        request: PatientConsentLifecycleRequest,
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
    ) -> WorkflowResult[PatientConsentLifecycleData]:
        """
        Execute the revoke transition.
        """
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            consent = _load_consent(
                context=context,
                consent_id=self._request.consent_id,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Patient consent was not found.",
            ) from exc

        if not self._policy.can_revoke(
            actor=actor,
            consent=consent,
        ):
            raise PermissionError(
                "You do not have permission to revoke this patient consent.",
            )

        previous = consent.status
        consent = revoke_consent(
            instance=consent,
            performed_by=actor,
        )

        event = PatientConsentStatusChangedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            consent_id=consent.pk,
            patient_id=consent.patient_id,
            organization_id=consent.organization_id,
            previous_status=previous,
            new_status=consent.status,
        )
        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientConsentLifecycleData(
                consent_id=consent.pk,
                patient_id=consent.patient_id,
                organization_id=consent.organization_id,
                previous_status=previous,
                new_status=consent.status,
                changed=True,
                event_id=event.event_id,
            ),
            message="Patient consent revoked successfully.",
            code="consent_revoked",
        )


class PatientConsentRestoreWorkflow(
    BaseWorkflow[PatientConsentLifecycleData],
):
    """
    Restore a deleted Patient Consent.
    """

    workflow_name = "consent.restore"

    def __init__(
        self,
        *,
        request: PatientConsentLifecycleRequest,
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
    ) -> WorkflowResult[PatientConsentLifecycleData]:
        """
        Execute the restore transition.
        """
        try:
            actor = User.objects.get(
                pk=context.actor_id,
            )
            consent = _load_consent(
                context=context,
                consent_id=self._request.consent_id,
                deleted=True,
            )
        except ObjectDoesNotExist as exc:
            raise ValueError(
                "Deleted patient consent was not found.",
            ) from exc

        if not self._policy.can_restore(
            actor=actor,
            consent=consent,
        ):
            raise PermissionError(
                "You do not have permission to restore this patient consent.",
            )

        previous = consent.status
        consent = restore_consent(
            instance=consent,
            performed_by=actor,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientConsentLifecycleData(
                consent_id=consent.pk,
                patient_id=consent.patient_id,
                organization_id=consent.organization_id,
                previous_status=previous,
                new_status=consent.status,
                changed=True,
            ),
            message="Patient consent restored successfully.",
            code="consent_restored",
        )


__all__ = (
    "PatientConsentGrantWorkflow",
    "PatientConsentLifecycleData",
    "PatientConsentLifecycleRequest",
    "PatientConsentRevokeWorkflow",
    "PatientConsentRestoreWorkflow",
)
