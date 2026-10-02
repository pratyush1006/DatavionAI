"""
Patient Core workflow registration.

This module registers the canonical Patient workflows with the
platform workflow registry.

Workflow names are stable application contracts.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.patients.workflows.patient_activation import (
    PatientActivationWorkflow,
)
from apps.patient_management.patients.workflows.patient_archive import (
    PatientArchiveWorkflow,
)
from apps.patient_management.patients.workflows.patient_creation import (
    PatientCreationWorkflow,
)
from apps.patient_management.patients.workflows.patient_deactivation import (
    PatientDeactivationWorkflow,
)
from apps.patient_management.patients.workflows.patient_deletion import (
    PatientDeletionWorkflow,
)
from apps.patient_management.patients.workflows.patient_restore import (
    PatientRestoreWorkflow,
)
from apps.patient_management.patients.workflows.patient_update import (
    PatientUpdateWorkflow,
)


def register_patient_workflows() -> None:
    """
    Register all canonical Patient workflows.

    Registration is idempotent so application startup can safely invoke
    this function more than once.
    """
    workflows = {
        "patient.create": PatientCreationWorkflow,
        "patient.update": PatientUpdateWorkflow,
        "patient.activate": PatientActivationWorkflow,
        "patient.deactivate": PatientDeactivationWorkflow,
        "patient.archive": PatientArchiveWorkflow,
        "patient.restore": PatientRestoreWorkflow,
        "patient.delete": PatientDeletionWorkflow,
    }

    for name, workflow in workflows.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("register_patient_workflows",)
