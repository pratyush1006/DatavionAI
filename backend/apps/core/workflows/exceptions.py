"""
Workflow exceptions.

Provides the exception hierarchy for workflow execution across the
DatavionAI platform.
"""

from __future__ import annotations

from typing import Any


class WorkflowError(Exception):
    """
    Base workflow exception.

    All workflow-related exceptions should inherit from this class.
    """

    def __init__(
        self,
        message: str,
        *,
        code: str = "workflow_error",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)

        self.message = message

        self.code = code

        self.details = details or {}

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize the exception.
        """

        return {
            "type": self.__class__.__name__,
            "code": self.code,
            "message": self.message,
            "details": self.details,
        }


class WorkflowConfigurationError(
    WorkflowError,
):
    """
    Raised when a workflow is incorrectly configured.
    """

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            code="workflow_configuration_error",
            details=details,
        )


class WorkflowValidationError(
    WorkflowError,
):
    """
    Raised when workflow validation fails.
    """

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            code="workflow_validation_error",
            details=details,
        )


class WorkflowExecutionError(
    WorkflowError,
):
    """
    Raised when workflow execution fails.
    """

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            code="workflow_execution_error",
            details=details,
        )


class WorkflowPolicyError(
    WorkflowExecutionError,
):
    """
    Raised when workflow policy validation fails.
    """

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            details=details,
        )

        self.code = "workflow_policy_error"


class WorkflowServiceError(
    WorkflowExecutionError,
):
    """
    Raised when a domain service fails during workflow execution.
    """

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            details=details,
        )

        self.code = "workflow_service_error"


class WorkflowEventError(
    WorkflowExecutionError,
):
    """
    Raised when domain event publication fails.
    """

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            details=details,
        )

        self.code = "workflow_event_error"


class WorkflowTaskError(
    WorkflowExecutionError,
):
    """
    Raised when a background task cannot be dispatched.
    """

    def __init__(
        self,
        message: str,
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            details=details,
        )

        self.code = "workflow_task_error"


class WorkflowTimeoutError(
    WorkflowExecutionError,
):
    """
    Raised when workflow execution exceeds the allowed timeout.
    """

    def __init__(
        self,
        message: str = "Workflow execution timed out.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            details=details,
        )

        self.code = "workflow_timeout_error"


class WorkflowCancelledError(
    WorkflowExecutionError,
):
    """
    Raised when a workflow is cancelled before completion.
    """

    def __init__(
        self,
        message: str = "Workflow execution cancelled.",
        *,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(
            message,
            details=details,
        )

        self.code = "workflow_cancelled_error"

    def __str__(
        self,
    ) -> str:
        """
        Human-readable exception representation.
        """

        return self.message

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"code={self.code!r}, "
            f"message={self.message!r}, "
            f"details={self.details!r}"
            ")"
        )


__all__: tuple[str, ...] = (
    "WorkflowCancelledError",
    "WorkflowConfigurationError",
    "WorkflowError",
    "WorkflowEventError",
    "WorkflowExecutionError",
    "WorkflowPolicyError",
    "WorkflowServiceError",
    "WorkflowTaskError",
    "WorkflowTimeoutError",
    "WorkflowValidationError",
)
