from __future__ import annotations

from apps.clinical.vitals.workflows import (
    VitalCreationWorkflow,
    VitalDeletionWorkflow,
    VitalUpdateWorkflow,
)
from apps.core.workflows import workflow_registry

VITAL_WORKFLOWS = {
    "vital.create": VitalCreationWorkflow,
    "vital.update": VitalUpdateWorkflow,
    "vital.delete": VitalDeletionWorkflow,
}


def register_vital_workflows() -> None:
    for name, workflow in VITAL_WORKFLOWS.items():
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


register_vital_workflows()
__all__ = ("VITAL_WORKFLOWS", "register_vital_workflows")
