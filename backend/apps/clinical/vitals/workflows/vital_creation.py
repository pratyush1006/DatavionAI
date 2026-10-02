from __future__ import annotations

import inspect
from typing import Any

from django.contrib.auth import get_user_model

from apps.clinical.encounters.models import Encounter
from apps.clinical.providers.models import Provider
from apps.clinical.vitals.services import create_vital
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


def _organization(
    context: WorkflowContext, organization_id: Any | None = None, instance=None
):
    if organization_id is not None:
        return Organization.objects.get(pk=organization_id, tenant_id=context.tenant_id)
    if instance is not None:
        organization = getattr(instance, "organization", None)
        if organization is not None and organization.tenant_id == context.tenant_id:
            return organization
    organization = Organization.objects.filter(tenant_id=context.tenant_id).first()
    if organization is None:
        raise Organization.DoesNotExist(
            "No organization is available for the workflow tenant."
        )
    return organization


def _invoke(function, *, organization, actor, instance=None, data=None):
    signature = inspect.signature(function)
    values = {
        "organization": organization,
        "organization_id": organization.id,
        "actor": actor,
        "performed_by": actor,
        "user": actor,
        "instance": instance,
        "vital": instance,
        "vital_instance": instance,
        "data": data,
        "validated_data": data,
        "vital_id": getattr(instance, "id", None),
        "object_id": getattr(instance, "id", None),
    }
    kwargs = {
        name: values[name]
        for name, param in signature.parameters.items()
        if name in values
        and values[name] is not None
        and (
            param.kind
            in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY)
        )
    }
    if "data" in signature.parameters and "data" not in kwargs:
        kwargs["data"] = data or {}
    return function(**kwargs)


from dataclasses import dataclass, field

from apps.clinical.vitals.events import VitalCreatedEvent
from apps.clinical.vitals.policies import VitalPolicy


@dataclass(frozen=True)
class VitalCreationRequest:
    organization_id: Any
    patient_id: Any
    provider_id: Any
    encounter_id: Any | None = None
    data: dict[str, Any] = field(default_factory=dict)


class VitalCreationWorkflow(BaseWorkflow):
    workflow_name = "vital.create"

    def __init__(self, *, request: VitalCreationRequest, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        organization = _organization(context, self.request.organization_id)
        actor = get_user_model().objects.get(pk=context.actor_id)
        if not VitalPolicy.can_create(user=actor, organization=organization):
            raise PermissionError("You do not have permission to create vitals.")
        payload = dict(self.request.data)
        payload["organization"] = organization
        payload["patient"] = Patient.objects.get(
            pk=self.request.patient_id, organization_id=organization.id
        )
        payload["provider"] = Provider.objects.get(
            pk=self.request.provider_id, organization_id=organization.id
        )
        if self.request.encounter_id is not None:
            payload["encounter"] = Encounter.objects.get(
                pk=self.request.encounter_id, organization_id=organization.id
            )
        vital = _invoke(
            create_vital, organization=organization, actor=actor, data=payload
        )
        self.publish_after_commit(
            VitalCreatedEvent(vital_id=vital.id, organization_id=organization.id)
        )
        return WorkflowResult.ok(
            context=context,
            data=vital,
            message="Vital created successfully.",
            code="vital_created",
        )
