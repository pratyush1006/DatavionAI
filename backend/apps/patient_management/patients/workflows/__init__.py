"""
Patient workflows.

Public application workflow API for the Patient bounded context.
"""

from __future__ import annotations

from apps.patient_management.patients.workflows.patient_activation import (
    PatientActivationData,
    PatientActivationRequest,
    PatientActivationWorkflow,
)
from apps.patient_management.patients.workflows.patient_archive import (
    PatientArchiveData,
    PatientArchiveRequest,
    PatientArchiveWorkflow,
)
from apps.patient_management.patients.workflows.patient_creation import (
    PatientCreationData,
    PatientCreationRequest,
    PatientCreationWorkflow,
)
from apps.patient_management.patients.workflows.patient_deactivation import (
    PatientDeactivationData,
    PatientDeactivationRequest,
    PatientDeactivationWorkflow,
)
from apps.patient_management.patients.workflows.patient_deletion import (
    PatientDeletionData,
    PatientDeletionRequest,
    PatientDeletionWorkflow,
)
from apps.patient_management.patients.workflows.patient_restore import (
    PatientRestoreData,
    PatientRestoreRequest,
    PatientRestoreWorkflow,
)
from apps.patient_management.patients.workflows.patient_update import (
    PatientUpdateData,
    PatientUpdateRequest,
    PatientUpdateWorkflow,
)

__all__: tuple[str, ...] = (
    "PatientActivationData",
    "PatientActivationRequest",
    "PatientActivationWorkflow",
    "PatientArchiveData",
    "PatientArchiveRequest",
    "PatientArchiveWorkflow",
    "PatientCreationData",
    "PatientCreationRequest",
    "PatientCreationWorkflow",
    "PatientDeactivationData",
    "PatientDeactivationRequest",
    "PatientDeactivationWorkflow",
    "PatientDeletionData",
    "PatientDeletionRequest",
    "PatientDeletionWorkflow",
    "PatientRestoreData",
    "PatientRestoreRequest",
    "PatientRestoreWorkflow",
    "PatientUpdateData",
    "PatientUpdateRequest",
    "PatientUpdateWorkflow",
)
