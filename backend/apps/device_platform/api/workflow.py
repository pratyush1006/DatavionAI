from __future__ import annotations

from apps.core.workflows import WorkflowContext, workflow_registry


def execute_device_workflow(
    *, request, organization, workflow_name: str, payload: dict
):
    workflow = workflow_registry.get(workflow_name)
    tenant_id = getattr(request.tenant, "tenant_id", None) or getattr(
        request.tenant, "pk", None
    )
    context = WorkflowContext.create(
        tenant_id=tenant_id, actor_id=request.user.pk, workflow_name=workflow_name
    )
    return workflow(payload=payload).execute(context=context)
