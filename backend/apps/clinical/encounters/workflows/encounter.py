from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.clinical.appointments.models import Appointment
from apps.clinical.encounters.constants import EncounterStatus
from apps.clinical.encounters.events import (
    EncounterCreated,
    EncounterDeleted,
    EncounterStatusChanged,
    EncounterUpdated,
)
from apps.clinical.encounters.policies import EncounterPolicy
from apps.clinical.encounters.selectors import get_encounter
from apps.clinical.encounters.services import EncounterService
from apps.clinical.providers.models import Provider
from apps.core.workflows import BaseWorkflow, WorkflowResult
from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class EncounterCreateRequest:
    organization_id: UUID
    appointment_id: UUID
    patient_id: UUID
    provider_id: UUID
    encounter_number: str
    data: dict


@dataclass(frozen=True, slots=True, kw_only=True)
class EncounterUpdateRequest:
    organization_id: UUID
    encounter_id: UUID
    data: dict


@dataclass(frozen=True, slots=True, kw_only=True)
class EncounterLifecycleRequest:
    organization_id: UUID
    encounter_id: UUID


def _resolve(context, organization_id, encounter_id=None):
    actor = User.objects.get(pk=context.actor_id)
    organization = Organization.objects.get(
        pk=organization_id,
        tenant_id=context.tenant_id,
    )
    record = None
    if encounter_id is not None:
        record = get_encounter(
            organization_id=organization.id,
            encounter_id=encounter_id,
        )
    return actor, organization, record


class EncounterCreateWorkflow(BaseWorkflow):
    workflow_name = "encounter.create"

    def __init__(self, *, request, policy=None, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or EncounterPolicy()

    @transaction.atomic
    def _run(self, *, context):
        actor, organization, _ = _resolve(context, self.request.organization_id)
        if not self.policy.can_create(actor=actor, organization=organization):
            raise PermissionError("User does not have permission to create encounters.")
        appointment = Appointment.objects.get(
            pk=self.request.appointment_id,
            organization_id=organization.id,
        )
        patient = Patient.objects.get(
            pk=self.request.patient_id,
            organization_id=organization.id,
        )
        provider = Provider.objects.get(
            pk=self.request.provider_id,
            organization_id=organization.id,
        )
        record = EncounterService.create(
            organization=organization,
            appointment=appointment,
            patient=patient,
            provider=provider,
            encounter_number=self.request.encounter_number,
            data=self.request.data,
        )
        self.publish_after_commit(
            EncounterCreated(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                encounter_id=record.id,
                organization_id=record.organization_id,
                patient_id=record.patient_id,
                provider_id=record.provider_id,
                appointment_id=record.appointment_id,
                status=record.status,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=record,
            message="Encounter created successfully.",
            code="encounter_created",
        )


class EncounterUpdateWorkflow(BaseWorkflow):
    workflow_name = "encounter.update"

    def __init__(self, *, request, policy=None, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or EncounterPolicy()

    @transaction.atomic
    def _run(self, *, context):
        actor, organization, record = _resolve(
            context,
            self.request.organization_id,
            self.request.encounter_id,
        )
        if not self.policy.can_update(actor=actor, organization=organization):
            raise PermissionError("User does not have permission to update encounters.")
        updated = EncounterService.update(
            encounter=record,
            data=self.request.data,
        )
        self.publish_after_commit(
            EncounterUpdated(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                encounter_id=updated.id,
                organization_id=updated.organization_id,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Encounter updated successfully.",
            code="encounter_updated",
        )


class _TransitionWorkflow(BaseWorkflow):
    target_status = None

    def __init__(self, *, request, policy=None, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or EncounterPolicy()

    @transaction.atomic
    def _run(self, *, context):
        actor, organization, record = _resolve(
            context,
            self.request.organization_id,
            self.request.encounter_id,
        )
        if not self.policy.can_transition(actor=actor, organization=organization):
            raise PermissionError(
                "User does not have permission to transition encounters."
            )
        previous = record.status
        updated = EncounterService.transition(
            encounter=record,
            target_status=self.target_status,
            actor_id=context.actor_id,
        )
        self.publish_after_commit(
            EncounterStatusChanged(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                encounter_id=updated.id,
                organization_id=updated.organization_id,
                previous_status=previous,
                new_status=updated.status,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message=f"Encounter moved to {updated.status}.",
            code="encounter_status_changed",
        )


class EncounterStartWorkflow(_TransitionWorkflow):
    workflow_name = "encounter.start"
    target_status = EncounterStatus.IN_PROGRESS


class EncounterCompleteWorkflow(_TransitionWorkflow):
    workflow_name = "encounter.complete"
    target_status = EncounterStatus.COMPLETED


class EncounterCancelWorkflow(_TransitionWorkflow):
    workflow_name = "encounter.cancel"
    target_status = EncounterStatus.CANCELLED


class EncounterDeleteWorkflow(BaseWorkflow):
    workflow_name = "encounter.delete"

    def __init__(self, *, request, policy=None, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or EncounterPolicy()

    @transaction.atomic
    def _run(self, *, context):
        actor, organization, record = _resolve(
            context,
            self.request.organization_id,
            self.request.encounter_id,
        )
        if not self.policy.can_delete(actor=actor, organization=organization):
            raise PermissionError("User does not have permission to delete encounters.")
        updated = EncounterService.delete(
            encounter=record,
            actor_id=context.actor_id,
        )
        self.publish_after_commit(
            EncounterDeleted(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                encounter_id=updated.id,
                organization_id=updated.organization_id,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Encounter deleted successfully.",
            code="encounter_deleted",
        )
