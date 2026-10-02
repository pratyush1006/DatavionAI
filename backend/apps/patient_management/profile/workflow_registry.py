"""
Patient Profile workflow registration.

Registers Patient Profile workflows into the DatavionOS
core workflow registry.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.profile.workflows import (
    ProfileCreationWorkflow,
    ProfileDeletionWorkflow,
    ProfileUpdateWorkflow,
)


def register_profile_workflows() -> None:
    """
    Register Patient Profile workflows.

    Workflow naming convention:

        <domain>.<capability>

    Examples:

        profile.create
        profile.update
        profile.delete
    """

    workflows = {
        #
        # Profile lifecycle
        #
        "profile.create": ProfileCreationWorkflow,
        "profile.update": ProfileUpdateWorkflow,
        "profile.delete": ProfileDeletionWorkflow,
    }

    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(
            name,
        ):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__: tuple[str, ...] = ("register_profile_workflows",)
