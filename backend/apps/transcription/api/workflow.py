"""
Canonical workflow execution adapter for API endpoints.
"""

from __future__ import annotations

from typing import Any

from apps.core.workflows import WorkflowContext


def execute_workflow(
    *,
    workflow_class,
    request,
    tenant,
    organization,
    workflow_name: str,
    payload: dict[str, Any],
):
    normalized = dict(payload)
    normalized["organization"] = organization
    normalized["organization_id"] = organization.id

    context = WorkflowContext.create(
        tenant_id=tenant.id,
        actor_id=request.user.id,
        workflow_name=workflow_name,
        request_id=getattr(request, "request_id", None),
        metadata={"organization_id": str(organization.id)},
    )

    return workflow_class(payload=normalized).execute(context=context)
