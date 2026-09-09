"""Workflow registration for Patient Communication."""

from __future__ import annotations

from apps.patient_management.communication.workflows.creation import (
    CommunicationCreationWorkflow,
)
from apps.patient_management.communication.workflows.deletion import (
    CommunicationDeletionWorkflow,
)
from apps.patient_management.communication.workflows.lifecycle import (
    CommunicationLifecycleWorkflow,
)
from apps.patient_management.communication.workflows.restore import (
    CommunicationRestoreWorkflow,
)
from apps.patient_management.communication.workflows.update import (
    CommunicationUpdateWorkflow,
)

WORKFLOW_NAMES = (
    "patient_communication.create",
    "patient_communication.update",
    "patient_communication.delete",
    "patient_communication.restore",
    "patient_communication.lifecycle",
)

__all__ = (
    "WORKFLOW_NAMES",
    "CommunicationCreationWorkflow",
    "CommunicationDeletionWorkflow",
    "CommunicationLifecycleWorkflow",
    "CommunicationRestoreWorkflow",
    "CommunicationUpdateWorkflow",
)
