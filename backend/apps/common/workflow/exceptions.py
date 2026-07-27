"""
Workflow exception hierarchy for DatavionOS.

Provides reusable exceptions for the workflow framework.
"""

from __future__ import annotations


class WorkflowError(
    Exception,
):
    """
    Base exception for workflow errors.
    """


class WorkflowConfigurationError(
    WorkflowError,
):
    """
    Raised when workflow configuration is invalid.
    """


class WorkflowNotFoundError(
    WorkflowError,
):
    """
    Raised when a workflow definition does not exist.
    """


class WorkflowAlreadyRegisteredError(
    WorkflowError,
):
    """
    Raised when registering an existing workflow.
    """


class WorkflowRegistrationError(
    WorkflowError,
):
    """
    Raised when workflow registration fails.
    """


class WorkflowStateError(
    WorkflowError,
):
    """
    Raised when workflow state is invalid.
    """


class InvalidTransitionError(
    WorkflowStateError,
):
    """
    Raised when a state transition is not allowed.
    """


class WorkflowExecutionError(
    WorkflowError,
):
    """
    Raised when workflow execution fails.
    """


class WorkflowContextError(
    WorkflowExecutionError,
):
    """
    Raised when workflow execution context is invalid.
    """


class WorkflowTimeoutError(
    WorkflowExecutionError,
):
    """
    Raised when workflow execution exceeds allowed time.
    """


__all__: tuple[str, ...] = (
    "InvalidTransitionError",
    "WorkflowAlreadyRegisteredError",
    "WorkflowConfigurationError",
    "WorkflowContextError",
    "WorkflowError",
    "WorkflowExecutionError",
    "WorkflowNotFoundError",
    "WorkflowRegistrationError",
    "WorkflowStateError",
    "WorkflowTimeoutError",
)
