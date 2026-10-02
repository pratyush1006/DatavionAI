"""Registration of Medical History workflows with the core registry."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.medical_history.workflows import (
    MedicalHistoryActivationWorkflow,
    MedicalHistoryCreationWorkflow,
    MedicalHistoryDeactivationWorkflow,
    MedicalHistoryDeletionWorkflow,
    MedicalHistoryRestoreWorkflow,
    MedicalHistoryUpdateWorkflow,
    MedicalHistoryVerificationWorkflow,
)

WORKFLOWS = {
    "medical_history.create": MedicalHistoryCreationWorkflow,
    "medical_history.update": MedicalHistoryUpdateWorkflow,
    "medical_history.delete": MedicalHistoryDeletionWorkflow,
    "medical_history.restore": MedicalHistoryRestoreWorkflow,
    "medical_history.activate": MedicalHistoryActivationWorkflow,
    "medical_history.deactivate": MedicalHistoryDeactivationWorkflow,
    "medical_history.verify": MedicalHistoryVerificationWorkflow,
}


def register_medical_history_workflows() -> None:
    """Register medical history workflows."""
    for name, workflow in WORKFLOWS.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


__all__ = (
    "WORKFLOWS",
    "register_medical_history_workflows",
)
