"""
Master Patient Index workflow registry integration.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.mpi.workflows import (
    MPICreationWorkflow,
    MPIDeletionWorkflow,
    MPILifecycleWorkflow,
    MPIMatchingWorkflow,
    MPIMergeWorkflow,
    MPIRestoreWorkflow,
    MPIReverseMergeWorkflow,
    MPIReviewWorkflow,
    MPIUpdateWorkflow,
)


def register_workflows() -> None:
    """Register all Master Patient Index workflows idempotently."""

    registrations = (
        ("patient_mpi.create", MPICreationWorkflow),
        ("patient_mpi.update", MPIUpdateWorkflow),
        ("patient_mpi.delete", MPIDeletionWorkflow),
        ("patient_mpi.restore", MPIRestoreWorkflow),
        ("patient_mpi.lifecycle", MPILifecycleWorkflow),
        ("patient_mpi.match", MPIMatchingWorkflow),
        ("patient_mpi.review", MPIReviewWorkflow),
        ("patient_mpi.merge", MPIMergeWorkflow),
        ("patient_mpi.reverse_merge", MPIReverseMergeWorkflow),
    )

    for name, workflow in registrations:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


register_workflows()

__all__ = ("register_workflows",)
