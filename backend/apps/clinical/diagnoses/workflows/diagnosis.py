from dataclasses import dataclass
from uuid import UUID

from django.db import transaction

from apps.clinical.diagnoses.events import (
    DiagnosisCreated,
    DiagnosisDeleted,
    DiagnosisUpdated,
)
from apps.clinical.diagnoses.policies import DiagnosisPolicy
from apps.clinical.diagnoses.selectors import get_diagnosis
from apps.clinical.diagnoses.services import DiagnosisService
from apps.clinical.encounters.models import Encounter
from apps.core.workflows import BaseWorkflow, WorkflowResult
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization


@dataclass(frozen=True, slots=True, kw_only=True)
class DiagnosisCreateRequest:
    organization_id: UUID
    encounter_id: UUID
    diagnosis_code: str
    diagnosis_type: str
    data: dict


@dataclass(frozen=True, slots=True, kw_only=True)
class DiagnosisUpdateRequest:
    organization_id: UUID
    diagnosis_id: UUID
    data: dict


@dataclass(frozen=True, slots=True, kw_only=True)
class DiagnosisDeleteRequest:
    organization_id: UUID
    diagnosis_id: UUID


def _resolve(context, organization_id, diagnosis_id=None):
    actor = User.objects.get(pk=context.actor_id)
    organization = Organization.objects.get(
        pk=organization_id, tenant_id=context.tenant_id
    )
    record = None
    if diagnosis_id is not None:
        record = get_diagnosis(
            organization_id=organization.id, diagnosis_id=diagnosis_id
        )
    return actor, organization, record


class DiagnosisCreateWorkflow(BaseWorkflow):
    workflow_name = "diagnosis.create"

    def __init__(self, *, request, policy=None, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or DiagnosisPolicy()

    @transaction.atomic
    def _run(self, *, context):
        actor, organization, _ = _resolve(context, self.request.organization_id)
        if not self.policy.can_create(actor=actor, organization=organization):
            raise PermissionError("User does not have permission to create diagnoses.")
        encounter = Encounter.objects.get(
            pk=self.request.encounter_id,
            organization_id=organization.id,
        )
        record = DiagnosisService.create(
            organization=organization,
            encounter=encounter,
            diagnosis_code=self.request.diagnosis_code,
            diagnosis_type=self.request.diagnosis_type,
            data=self.request.data,
        )
        self.publish_after_commit(
            DiagnosisCreated(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                diagnosis_id=record.id,
                organization_id=record.organization_id,
                encounter_id=record.encounter_id,
                diagnosis_code=record.diagnosis_code,
                status=record.status,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=record,
            message="Diagnosis created successfully.",
            code="diagnosis_created",
        )


class DiagnosisUpdateWorkflow(BaseWorkflow):
    workflow_name = "diagnosis.update"

    def __init__(self, *, request, policy=None, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or DiagnosisPolicy()

    @transaction.atomic
    def _run(self, *, context):
        actor, organization, record = _resolve(
            context,
            self.request.organization_id,
            self.request.diagnosis_id,
        )
        if not self.policy.can_update(actor=actor, organization=organization):
            raise PermissionError("User does not have permission to update diagnoses.")
        updated = DiagnosisService.update(diagnosis=record, data=self.request.data)
        self.publish_after_commit(
            DiagnosisUpdated(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                diagnosis_id=updated.id,
                organization_id=updated.organization_id,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Diagnosis updated successfully.",
            code="diagnosis_updated",
        )


class DiagnosisDeleteWorkflow(BaseWorkflow):
    workflow_name = "diagnosis.delete"

    def __init__(self, *, request, policy=None, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request
        self.policy = policy or DiagnosisPolicy()

    @transaction.atomic
    def _run(self, *, context):
        actor, organization, record = _resolve(
            context,
            self.request.organization_id,
            self.request.diagnosis_id,
        )
        if not self.policy.can_delete(actor=actor, organization=organization):
            raise PermissionError("User does not have permission to delete diagnoses.")
        deleted = DiagnosisService.delete(diagnosis=record, actor_id=context.actor_id)
        self.publish_after_commit(
            DiagnosisDeleted(
                tenant_id=context.tenant_id,
                actor_id=context.actor_id,
                diagnosis_id=deleted.id,
                organization_id=deleted.organization_id,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=deleted,
            message="Diagnosis deleted successfully.",
            code="diagnosis_deleted",
        )
