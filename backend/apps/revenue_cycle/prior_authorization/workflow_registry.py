"""
Revenue Cycle Prior Authorization workflow registration.

Registration is explicit and idempotent. The module deliberately does not
register workflows during import so it remains safe during Django application
initialization.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.revenue_cycle.prior_authorization.workflows import (
    PriorAuthorizationCreationWorkflow,
    PriorAuthorizationDeletionWorkflow,
    PriorAuthorizationLifecycleWorkflow,
    PriorAuthorizationRestoreWorkflow,
    PriorAuthorizationUpdateWorkflow,
)

WORKFLOW_DEFINITIONS = (
    (
        "revenue_cycle.prior_authorization.create",
        PriorAuthorizationCreationWorkflow,
    ),
    (
        "revenue_cycle.prior_authorization.update",
        PriorAuthorizationUpdateWorkflow,
    ),
    (
        "revenue_cycle.prior_authorization.delete",
        PriorAuthorizationDeletionWorkflow,
    ),
    (
        "revenue_cycle.prior_authorization.restore",
        PriorAuthorizationRestoreWorkflow,
    ),
    (
        "revenue_cycle.prior_authorization.lifecycle",
        PriorAuthorizationLifecycleWorkflow,
    ),
)


def register_workflows() -> None:
    """
    Register Prior Authorization workflows idempotently.

    This function must be called by the Revenue Cycle AppConfig ``ready()``
    hook rather than during module import.
    """

    for name, workflow in WORKFLOW_DEFINITIONS:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__: tuple[str, ...] = (
    "WORKFLOW_DEFINITIONS",
    "register_workflows",
)
