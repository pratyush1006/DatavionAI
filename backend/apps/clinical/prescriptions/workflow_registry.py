"""Canonical workflow registration boundary for Prescription."""

from __future__ import annotations

from apps.core.workflows import workflow_registry

from .workflows import (
    PrescriptionCreateWorkflow,
    PrescriptionDeleteWorkflow,
    PrescriptionLifecycleWorkflow,
    PrescriptionUpdateWorkflow,
)


def register_prescription_workflows() -> None:
    """Register only the fresh workflow surface for this bounded context."""
    workflows = (
        ("prescription.create", PrescriptionCreateWorkflow),
        ("prescription.update", PrescriptionUpdateWorkflow),
        ("prescription.delete", PrescriptionDeleteWorkflow),
        ("prescription.lifecycle", PrescriptionLifecycleWorkflow),
    )
    for name, workflow in workflows:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(name=name, workflow=workflow)


__all__ = ("register_prescription_workflows",)
