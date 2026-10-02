"""
Patient Consent creation workflow.
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
from apps.patient_management.consents.events import (
    PatientConsentCreatedEvent,
)
from apps.patient_management.consents.policies import (
    PatientConsentPolicy,
)
from apps.patient_management.consents.services import (
    create_consent,
)
from apps.patient_management.patients.models import (
    Patient,
)
from apps.platform.accounts.models import (
    User,
)
from apps.platform.organizations.models import (
    Organization,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientConsentCreationRequest:
    """
    Input required to create a Patient Consent.
    """

    organization_id: UUID
    patient_id: UUID
    data: Mapping[str, Any]


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class PatientConsentCreationData:
    """
    Result returned after Patient Consent creation.
    """

    consent_id: UUID
    patient_id: UUID
    organization_id: UUID
    created: bool
    event_id: UUID | None = None


class PatientConsentCreationWorkflow(
    BaseWorkflow[PatientConsentCreationData],
):
    """
    Create a Patient Consent within the current tenant.
    """

    workflow_name = "consent.create"

    def __init__(
        self,
        *,
        request: PatientConsentCreationRequest,
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
    ) -> WorkflowResult[PatientConsentCreationData]:
        """
        Execute the Patient Consent creation workflow.
        """
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
                "You do not have permission to create a patient consent.",
            )

        data = dict(
            self._request.data,
        )
        data["organization"] = organization
        data["patient"] = patient

        consent = create_consent(
            validated_data=data,
            performed_by=actor,
        )

        event = PatientConsentCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            consent_id=consent.pk,
            patient_id=consent.patient_id,
            organization_id=consent.organization_id,
            purpose=consent.purpose,
            status=consent.status,
        )

        self.publish_after_commit(
            event,
        )

        return WorkflowResult.ok(
            context=context,
            data=PatientConsentCreationData(
                consent_id=consent.pk,
                patient_id=consent.patient_id,
                organization_id=consent.organization_id,
                created=True,
                event_id=event.event_id,
            ),
            message="Patient consent created successfully.",
            code="consent_created",
        )


__all__ = (
    "PatientConsentCreationData",
    "PatientConsentCreationRequest",
    "PatientConsentCreationWorkflow",
)
