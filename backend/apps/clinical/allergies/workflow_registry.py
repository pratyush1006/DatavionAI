"""Idempotent Clinical Allergies workflow registration."""

from __future__ import annotations

from apps.clinical.allergies.workflows import (
    AllergyCreationWorkflow,
    AllergyDeletionWorkflow,
    AllergyUpdateWorkflow,
)
from apps.core.workflows import workflow_registry

ALLERGY_WORKFLOWS = {
    "allergy.create": AllergyCreationWorkflow,
    "allergy.update": AllergyUpdateWorkflow,
    "allergy.delete": AllergyDeletionWorkflow,
}


def register_allergy_workflows() -> None:
    for name, workflow in ALLERGY_WORKFLOWS.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


register_allergy_workflows()

__all__ = ("ALLERGY_WORKFLOWS", "register_allergy_workflows")
