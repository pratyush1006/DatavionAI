"""
Workflow service aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.workflow.engine import (
    WorkflowEngine,
)
from apps.datavionos.workflow.registry import (
    WorkflowRegistry,
)


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowServices:
    """
    Aggregate of workflow services.
    """

    registry: WorkflowRegistry

    engine: WorkflowEngine


__all__ = [
    "WorkflowServices",
]
