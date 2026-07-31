"""
Workflow exceptions.
"""

from __future__ import annotations


class WorkflowError(Exception):
    """Base workflow error."""


class WorkflowNotFoundError(WorkflowError):
    """Workflow definition not found."""


class WorkflowAlreadyRegisteredError(WorkflowError):
    """Workflow already registered."""


class WorkflowExecutionError(WorkflowError):
    """Workflow execution failed."""


class WorkflowTransitionError(WorkflowError):
    """Invalid workflow transition."""


class WorkflowStepError(WorkflowError):
    """Workflow step execution failed."""


class WorkflowEngineError(WorkflowError):
    """Workflow engine failure."""


class WorkflowValidationError(WorkflowError):
    """Workflow definition is invalid."""


__all__ = [
    "WorkflowError",
    "WorkflowNotFoundError",
    "WorkflowAlreadyRegisteredError",
    "WorkflowExecutionError",
    "WorkflowTransitionError",
    "WorkflowStepError",
    "WorkflowEngineError",
    "WorkflowValidationError",
]
