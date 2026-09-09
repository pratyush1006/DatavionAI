"""Medical History Creation."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from uuid import UUID

from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.medical_history.events import MedicalHistoryCreatedEvent
from apps.patient_management.medical_history.policies import MedicalHistoryPolicy
from apps.patient_management.medical_history.services import create_medical_history
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class MedicalHistoryCreationRequest:
    """MedicalHistoryCreationRequest implementation."""

    organization_id: UUID
    patient_id: UUID
    data: Mapping


@dataclass(frozen=True, slots=True, kw_only=True)
class MedicalHistoryCreationData:
    """MedicalHistoryCreationData implementation."""

    history_id: UUID
    patient_id: UUID
    organization_id: UUID
    created: bool
    event_id: UUID | None = None


class MedicalHistoryCreationWorkflow(BaseWorkflow[MedicalHistoryCreationData]):
    """MedicalHistoryCreationWorkflow implementation."""

    workflow_name = "medical_history.create"

    def __init__(
        self,
        *,
        request: MedicalHistoryCreationRequest,
        policy: MedicalHistoryPolicy | None = None,
        logger_=None,
    ) -> None:
        """init  ."""
        super().__init__(logger_=logger_, payload=request)
        self._request = request
        self._policy = policy or MedicalHistoryPolicy()

    @transaction.atomic
    def _run(
        self, context: WorkflowContext
    ) -> WorkflowResult[MedicalHistoryCreationData]:
        """run."""
        try:
            actor = User.objects.get(pk=context.actor_id)
            organization = Organization.objects.get(
                pk=self._request.organization_id, tenant_id=context.tenant_id
            )
            patient = Patient.objects.get(
                pk=self._request.patient_id, organization_id=organization.pk
            )
        except ObjectDoesNotExist as exc:
            raise ValueError("Organization or patient was not found.") from exc
        if not self._policy.can_create(actor=actor, organization=organization):
            raise PermissionError(
                "You do not have permission to create medical history."
            )
        data = dict(self._request.data)
        data.update(organization=organization, patient=patient)
        history = create_medical_history(validated_data=data, performed_by=actor)
        event = MedicalHistoryCreatedEvent(
            tenant_id=context.tenant_id,
            actor_id=actor.pk,
            history_id=history.pk,
            patient_id=history.patient_id,
            organization_id=history.organization_id,
            history_type=history.history_type,
            clinical_status=history.clinical_status,
        )
        self.publish_after_commit(event)
        return WorkflowResult.ok(
            context=context,
            data=MedicalHistoryCreationData(
                history_id=history.pk,
                patient_id=history.patient_id,
                organization_id=history.organization_id,
                created=True,
                event_id=event.event_id,
            ),
            message="Medical history created successfully.",
            code="medical_history_created",
        )


__all__ = (
    "MedicalHistoryCreationRequest",
    "MedicalHistoryCreationData",
    "MedicalHistoryCreationWorkflow",
)
