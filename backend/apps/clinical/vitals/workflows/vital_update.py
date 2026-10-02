from __future__ import annotations

import inspect
from typing import Any

from django.contrib.auth import get_user_model

from apps.clinical.vitals.services import update_vital
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
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

from apps.clinical.vitals.events import VitalUpdatedEvent
from apps.clinical.vitals.models import Vital
from apps.clinical.vitals.policies import VitalPolicy


@dataclass(frozen=True)
class VitalUpdateRequest:
    vital_id: Any
    data: dict[str, Any] = field(default_factory=dict)


class VitalUpdateWorkflow(BaseWorkflow):
    workflow_name = "vital.update"

    def __init__(self, *, request: VitalUpdateRequest, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        organization = _organization(context)
        actor = get_user_model().objects.get(pk=context.actor_id)
        vital = Vital.objects.select_related("organization").get(
            pk=self.request.vital_id,
            organization_id=organization.id,
        )
        if not VitalPolicy.can_update(user=actor, organization=organization):
            raise PermissionError("You do not have permission to update vitals.")
        updated = _invoke(
            update_vital,
            organization=organization,
            actor=actor,
            instance=vital,
            data=self.request.data,
        )
        self.publish_after_commit(
            VitalUpdatedEvent(
                vital_id=updated.id,
                organization_id=organization.id,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=updated,
            message="Vital updated successfully.",
            code="vital_updated",
        )
