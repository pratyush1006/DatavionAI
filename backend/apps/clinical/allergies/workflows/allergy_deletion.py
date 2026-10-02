from __future__ import annotations

import inspect
from typing import Any

from apps.clinical.allergies.models import Allergy
from apps.clinical.allergies.services import (
    delete_allergy,
)
from apps.core.workflows import BaseWorkflow, WorkflowContext, WorkflowResult
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


from dataclasses import dataclass

from apps.clinical.allergies.events import AllergyDeletedEvent
from apps.clinical.allergies.policies import AllergyPolicy


@dataclass(frozen=True)
class AllergyDeletionRequest:
    allergy_id: Any
    organization_id: Any


class AllergyDeletionWorkflow(BaseWorkflow):
    workflow_name = "allergy.delete"

    def __init__(self, *, request: AllergyDeletionRequest, logger_=None):
        super().__init__(logger_=logger_, payload=request)
        self.request = request

    def _run(self, context: WorkflowContext) -> WorkflowResult:
        organization = _organization(context, self.request.organization_id)
        actor = _actor(context)
        allergy = Allergy.objects.get(
            pk=self.request.allergy_id,
            organization_id=organization.id,
        )
        if not AllergyPolicy.can_delete(user=actor, organization=organization):
            raise PermissionError("You do not have permission to delete allergies.")
        deleted = _invoke(
            delete_allergy,
            organization=organization,
            actor=actor,
            instance=allergy,
        )
        self.publish_after_commit(
            AllergyDeletedEvent(
                allergy_id=deleted.id,
                organization_id=organization.id,
            )
        )
        return WorkflowResult.ok(
            context=context,
            data=deleted,
            message="Allergy deleted successfully.",
            code="allergy_deleted",
        )
