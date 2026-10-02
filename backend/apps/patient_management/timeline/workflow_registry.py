"""
Workflow registrations for Patient Timeline.
"""

from __future__ import annotations

from apps.core.workflows import workflow_registry
from apps.patient_management.timeline.workflows import (
    TimelineCreationWorkflow,
    TimelineDeletionWorkflow,
    TimelineLifecycleWorkflow,
    TimelineRestoreWorkflow,
    TimelineUpdateWorkflow,
)


def register_timeline_workflows() -> None:
    """Register all Patient Timeline workflows."""

    registrations = (
        (
            "timeline.create",
            TimelineCreationWorkflow,
        ),
        (
            "timeline.update",
            TimelineUpdateWorkflow,
        ),
        (
            "timeline.delete",
            TimelineDeletionWorkflow,
        ),
        (
            "timeline.lifecycle",
            TimelineLifecycleWorkflow,
        ),
        (
            "timeline.restore",
            TimelineRestoreWorkflow,
        ),
    )

    for name, workflow in registrations:
        if not workflow_registry.is_registered(name):
            workflow_registry.register(
                name=name,
                workflow=workflow,
            )


__all__ = ("register_timeline_workflows",)
