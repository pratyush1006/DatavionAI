from __future__ import annotations

import inspect
from typing import Any

from apps.clinical.allergies.services import (
    create_allergy,
)
from apps.clinical.encounters.models import Encounter
from apps.clinical.providers.models import Provider
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
from apps.patient_management.patients.models import Patient
from apps.platform.organizations.models import Organization


def _organization(context: WorkflowContext, organization_id: Any = None):
    resolved_id = organization_id or getattr(context, "tenant_id", None)
    if resolved_id is None:
        raise ValueError("Workflow organization is required.")
    return Organization.objects.get(pk=resolved_id)


def _actor(context: WorkflowContext):
    from apps.platform.accounts.models import User

    actor_id = getattr(context, "actor_id", None)
    if actor_id is None:
        raise ValueError("Workflow actor is required.")
    return User.objects.get(pk=actor_id)


def _invoke(function, *, organization, actor, instance=None, data=None):
    signature = inspect.signature(function)
    values = {
        "organization": organization,
        "organization_id": getattr(organization, "id", None),
        "actor": actor,
        "performed_by": actor,
        "user": actor,
        "instance": instance,
        "allergy": instance,
        "allergy_instance": instance,
        "data": data,
        "validated_data": data,
        "allergy_id": getattr(instance, "id", None),
        "object_id": getattr(instance, "id", None),
    }
    kwargs = {
        name: values[name]
        for name, parameter in signature.parameters.items()
        if name in values
        and values[name] is not None
        and parameter.kind
        in (
            inspect.Parameter.POSITIONAL_OR_KEYWORD,
            inspect.Parameter.KEYWORD_ONLY,
        )
    }
    if "data" in signature.parameters and "data" not in kwargs:
        kwargs["data"] = data or {}
    return function(**kwargs)


from dataclasses import dataclass, field

from apps.clinical.allergies.events import AllergyCreatedEvent
from apps.clinical.allergies.policies import AllergyPolicy


@dataclass(frozen=True)
class AllergyCreationRequest:
    organization_id: Any
    patient_id: Any
    provider_id: Any | None = None
    encounter_id: Any | None = None
    data: dict[str, Any] = field(default_factory=dict)


class AllergyCreationWorkflow(BaseWorkflow):
    workflow_name = "allergy.create"

    def __init__(self, *, request: AllergyCreationRequest, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        organization = _organization(context, self.request.organization_id)
        actor = _actor(context)
        if not AllergyPolicy.can_create(user=actor, organization=organization):
            raise PermissionError("You do not have permission to create allergies.")
        payload = dict(self.request.data)
        payload["organization"] = organization
        payload["patient"] = Patient.objects.get(
            pk=self.request.patient_id,
            organization_id=organization.id,
        )
        if self.request.provider_id is not None:
            payload["provider"] = Provider.objects.get(
                pk=self.request.provider_id,
                organization_id=organization.id,
            )
        encounter_id = (
            self.request.encounter_id
            or payload.get("encounter")
            or payload.get("encounter_id")
        )
        if encounter_id is None:
            raise ValueError("Encounter is required to create an allergy.")
        if hasattr(encounter_id, "id"):
            encounter = encounter_id
            if (
                getattr(encounter, "organization_id", organization.id)
                != organization.id
            ):
                raise ValueError(
                    "Encounter does not belong to the selected organization."
                )
        else:
            encounter = Encounter.objects.get(
                pk=encounter_id,
                organization_id=organization.id,
            )
        payload["encounter"] = encounter
        allergy = create_allergy(
            organization=organization,
            patient=payload["patient"],
            provider=payload.get("provider"),
            encounter=encounter,
            actor=actor,
            data=payload,
        )
        self.publish_after_commit(
            AllergyCreatedEvent(
                allergy_id=allergy.id,
                organization_id=organization.id,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=allergy,
            message="Allergy created successfully.",
            code="allergy_created",
        )
