"""Workflow registration for patient emergency management."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.emergency.workflows import (
    EmergencyCreationWorkflow,
    EmergencyDeletionWorkflow,
    EmergencyLifecycleWorkflow,
    EmergencyUpdateWorkflow,
)


def register_workflows() -> None:
    """Register all emergency workflows with the platform registry."""

    registrations = (
        ("emergency.create", EmergencyCreationWorkflow),
        ("emergency.update", EmergencyUpdateWorkflow),
        ("emergency.delete", EmergencyDeletionWorkflow),
        ("emergency.lifecycle", EmergencyLifecycleWorkflow),
    )

    for name, workflow in registrations:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("register_workflows",)
