"""Workflow registrations for Patient Preferences."""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.preferences.workflows import (
    PatientCommunicationPreferenceWorkflow,
    PatientPreferenceCreationWorkflow,
    PatientPreferenceDeletionWorkflow,
    PatientPreferenceRestoreWorkflow,
    PatientPreferenceUpdateWorkflow,
)


def register_patient_preference_workflows() -> None:
    """Register all Patient Preferences workflows."""

    registrations = {
        "patient_preferences.create": PatientPreferenceCreationWorkflow,
        "patient_preferences.update": PatientPreferenceUpdateWorkflow,
        "patient_preferences.delete": PatientPreferenceDeletionWorkflow,
        "patient_preferences.restore": PatientPreferenceRestoreWorkflow,
        "patient_preferences.communication_update": PatientCommunicationPreferenceWorkflow,
    }

    for name, workflow in registrations.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


register_patient_preference_workflows()

__all__ = ("register_patient_preference_workflows",)
