from __future__ import annotations

from apps.core.workflows.registry import workflow_registry
from apps.patient_management.relationships.workflows import (
    PatientRelationshipActivationWorkflow,
    PatientRelationshipCreationWorkflow,
    PatientRelationshipDeactivationWorkflow,
    PatientRelationshipDeletionWorkflow,
    PatientRelationshipRestoreWorkflow,
    PatientRelationshipSetPrimaryWorkflow,
    PatientRelationshipTerminateWorkflow,
    PatientRelationshipUpdateWorkflow,
    PatientRelationshipVerifyWorkflow,
)

WORKFLOW_DEFINITIONS = (
    ("relationship.create", PatientRelationshipCreationWorkflow),
    ("relationship.update", PatientRelationshipUpdateWorkflow),
    ("relationship.delete", PatientRelationshipDeletionWorkflow),
    ("relationship.restore", PatientRelationshipRestoreWorkflow),
    ("relationship.activate", PatientRelationshipActivationWorkflow),
    ("relationship.deactivate", PatientRelationshipDeactivationWorkflow),
    ("relationship.verify", PatientRelationshipVerifyWorkflow),
    ("relationship.terminate", PatientRelationshipTerminateWorkflow),
    ("relationship.set_primary", PatientRelationshipSetPrimaryWorkflow),
)


def register_patient_relationship_workflows():
    for name, workflow in WORKFLOW_DEFINITIONS:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


register_patient_relationship_workflows()
