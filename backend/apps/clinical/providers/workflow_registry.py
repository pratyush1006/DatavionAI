"""
Provider workflow registration.

Registers provider workflows into the DatavionOS
core workflow registry.
"""

from __future__ import annotations

from apps.clinical.providers.workflows import (
    ProviderActivationWorkflow,
    ProviderAssignmentWorkflow,
    ProviderCreationWorkflow,
    ProviderDeactivationWorkflow,
    ProviderUpdateWorkflow,
    ProviderVerificationWorkflow,
)
from apps.core.workflows import (
    workflow_registry,
)


def register_provider_workflows() -> None:
    """
    Register provider workflows.

    Workflow naming convention:

        <domain>.<capability>

    Examples:

        provider.create
        provider.verify
        provider.assign
    """

    workflows = {
        #
        # Provider lifecycle
        #
        "provider.create": (ProviderCreationWorkflow),
        "provider.update": (ProviderUpdateWorkflow),
        "provider.verify": (ProviderVerificationWorkflow),
        "provider.activate": (ProviderActivationWorkflow),
        "provider.deactivate": (ProviderDeactivationWorkflow),
        #
        # Organization / clinical structure
        #
        "provider.assign": (ProviderAssignmentWorkflow),
    }

    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(
            name,
        ):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__: tuple[str, ...] = ("register_provider_workflows",)
