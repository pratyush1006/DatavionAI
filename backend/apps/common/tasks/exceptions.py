"""
Task exception hierarchy for DatavionOS.

Provides reusable exceptions for the platform task framework.

The hierarchy supports:

- Configuration failures
- Payload validation failures
- Task registration failures
- Execution failures
- Queue/backend failures
"""

from __future__ import annotations


class TaskError(
    Exception,
):
    """
    Base exception for all task-related errors.
    """


class TaskConfigurationError(
    TaskError,
):
    """
    Raised when task configuration is invalid.
    """


class TaskPayloadError(
    TaskError,
):
    """
    Raised when task payload validation fails.
    """


class TaskRegistrationError(
    TaskError,
):
    """
    Raised when task registration fails.
    """


class TaskAlreadyRegisteredError(
    TaskRegistrationError,
):
    """
    Raised when a task is registered more than once.
    """


class TaskNotRegisteredError(
    TaskRegistrationError,
):
    """
    Raised when a task cannot be found in the registry.
    """


class TaskExecutionError(
    TaskError,
):
    """
    Raised when task execution fails.
    """


class TaskTimeoutError(
    TaskExecutionError,
):
    """
    Raised when a task exceeds its execution timeout.
    """


class TaskRetryError(
    TaskExecutionError,
):
    """
    Raised when task retry handling fails.
    """


class TaskCancelledError(
    TaskExecutionError,
):
    """
    Raised when a task is cancelled.
    """


class TaskBackendError(
    TaskExecutionError,
):
    """
    Raised when task execution backend fails.

    Examples:

    - Queue unavailable
    - Worker unavailable
    - Broker connection failure
    - Redis/Celery failure
    """


__all__: tuple[str, ...] = (
    "TaskAlreadyRegisteredError",
    "TaskBackendError",
    "TaskCancelledError",
    "TaskConfigurationError",
    "TaskError",
    "TaskExecutionError",
    "TaskNotRegisteredError",
    "TaskPayloadError",
    "TaskRegistrationError",
    "TaskRetryError",
    "TaskTimeoutError",
)
