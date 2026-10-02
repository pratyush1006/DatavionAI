from __future__ import annotations

import inspect
from typing import Any

from django.contrib.auth import get_user_model

from apps.clinical.vitals.services import delete_vital
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


from dataclasses import dataclass

from apps.clinical.vitals.events import VitalDeletedEvent
from apps.clinical.vitals.models import Vital
from apps.clinical.vitals.policies import VitalPolicy


@dataclass(frozen=True)
class VitalDeletionRequest:
    vital_id: Any


class VitalDeletionWorkflow(BaseWorkflow):
    workflow_name = "vital.delete"

    def __init__(self, *, request: VitalDeletionRequest, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        organization = _organization(context)
        actor = get_user_model().objects.get(pk=context.actor_id)
        vital = Vital.objects.select_related("organization").get(
            pk=self.request.vital_id,
            organization_id=organization.id,
        )
        if not VitalPolicy.can_delete(user=actor, organization=organization):
            raise PermissionError("You do not have permission to delete vitals.")
        deleted = _invoke(
            delete_vital,
            organization=organization,
            actor=actor,
            instance=vital,
        )
        deleted = deleted if deleted is not None else vital
        self.publish_after_commit(
            VitalDeletedEvent(
                vital_id=vital.id,
                organization_id=organization.id,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=deleted,
            message="Vital deleted successfully.",
            code="vital_deleted",
        )
