"""
Workflow result.

Provides the standardized workflow result object used throughout
the DatavionAI platform.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from typing import Any, TypeVar

from apps.core.workflows.context import WorkflowContext
from apps.core.workflows.exceptions import WorkflowError

T = TypeVar("T")
U = TypeVar("U")


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class WorkflowResult[T]:
    """
    Standard workflow result.

    Every workflow should return this object.

    The result is immutable and contains both the execution outcome
    and contextual metadata for tracing and auditing.
    """

    success: bool

    context: WorkflowContext

    data: T | None = None

    message: str | None = None

    code: str | None = None

    error: WorkflowError | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    warnings: tuple[str, ...] = ()

    occurred_at: datetime = field(
        default_factory=lambda: datetime.now(UTC),
    )

    duration_ms: int | None = None

    @classmethod
    def ok(
        cls,
        *,
        context: WorkflowContext,
        data: T | None = None,
        message: str | None = None,
        code: str | None = None,
        metadata: dict[str, Any] | None = None,
        warnings: tuple[str, ...] = (),
        duration_ms: int | None = None,
    ) -> WorkflowResult[T]:
        """
        Create a successful workflow result.
        """

        return cls(
            success=True,
            context=context,
            data=data,
            message=message,
            code=code,
            metadata=metadata or {},
            warnings=warnings,
            duration_ms=duration_ms,
        )

    @classmethod
    def fail(
        cls,
        *,
        context: WorkflowContext,
        message: str,
        code: str,
        error: WorkflowError | None = None,
        metadata: dict[str, Any] | None = None,
        duration_ms: int | None = None,
    ) -> WorkflowResult[T]:
        """
        Create a failed workflow result.
        """

        return cls(
            success=False,
            context=context,
            message=message,
            code=code,
            error=error,
            metadata=metadata or {},
            duration_ms=duration_ms,
        )

    @classmethod
    def warning(
        cls,
        *,
        context: WorkflowContext,
        data: T | None = None,
        message: str | None = None,
        warnings: tuple[str, ...] = (),
        metadata: dict[str, Any] | None = None,
        duration_ms: int | None = None,
    ) -> WorkflowResult[T]:
        """
        Create a successful workflow result containing warnings.
        """

        return cls(
            success=True,
            context=context,
            data=data,
            message=message,
            metadata=metadata or {},
            warnings=warnings,
            duration_ms=duration_ms,
        )

    @classmethod
    def from_exception(
        cls,
        *,
        context: WorkflowContext,
        exception: WorkflowError,
        duration_ms: int | None = None,
    ) -> WorkflowResult[T]:
        """
        Create a workflow result from a WorkflowError.
        """

        return cls(
            success=False,
            context=context,
            message=exception.message,
            code=exception.code,
            error=exception,
            metadata=exception.details,
            duration_ms=duration_ms,
        )

    @property
    def is_success(
        self,
    ) -> bool:
        """
        Whether the workflow completed successfully.
        """

        return self.success

    @property
    def is_failure(
        self,
    ) -> bool:
        """
        Whether the workflow failed.
        """

        return not self.success

    @property
    def has_error(
        self,
    ) -> bool:
        """
        Whether the workflow contains an error.
        """

        return self.error is not None

    @property
    def has_warnings(
        self,
    ) -> bool:
        """
        Whether warnings are present.
        """

        return len(self.warnings) > 0

    def unwrap(
        self,
    ) -> T:
        """
        Return the workflow data.

        Raises:
            WorkflowError:
                If the workflow failed.
            ValueError:
                If the workflow succeeded but contains no data.
        """

        self.ensure_success()

        if self.data is None:
            raise ValueError(
                "Workflow completed successfully but returned no data.",
            )

        return self.data

    def ensure_success(
        self,
    ) -> None:
        """
        Ensure the workflow completed successfully.

        Raises:
            WorkflowError:
                The underlying workflow error if present.
            RuntimeError:
                A generic runtime error if the workflow failed without
                an associated WorkflowError.
        """

        if self.success:
            return

        if self.error is not None:
            raise self.error

        raise RuntimeError(
            self.message or "Workflow execution failed.",
        )

    def map(
        self,
        mapper: callable[[T], U],
    ) -> WorkflowResult[U]:
        """
        Transform the workflow data while preserving the workflow
        result metadata.

        The mapper is only invoked for successful results containing
        data.
        """

        if not self.success:
            return WorkflowResult.fail(
                context=self.context,
                message=self.message or "Workflow failed.",
                code=self.code or "workflow_failed",
                error=self.error,
                metadata=self.metadata,
                duration_ms=self.duration_ms,
            )

        if self.data is None:
            return WorkflowResult.ok(
                context=self.context,
                message=self.message,
                code=self.code,
                metadata=self.metadata,
                warnings=self.warnings,
                duration_ms=self.duration_ms,
            )

        return WorkflowResult.ok(
            context=self.context,
            data=mapper(self.data),
            message=self.message,
            code=self.code,
            metadata=self.metadata,
            warnings=self.warnings,
            duration_ms=self.duration_ms,
        )

    def with_metadata(
        self,
        **metadata: Any,
    ) -> WorkflowResult[T]:
        """
        Return a new immutable result with merged metadata.
        """

        return replace(
            self,
            metadata={
                **self.metadata,
                **metadata,
            },
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize the workflow result.

        This representation is intended for structured logging,
        auditing, and diagnostics.
        """

        if hasattr(self.data, "to_dict"):
            payload = self.data.to_dict()
        elif hasattr(self.data, "__dict__"):
            payload = vars(self.data)
        else:
            payload = self.data

        return {
            "success": self.success,
            "message": self.message,
            "code": self.code,
            "context": self.context.to_dict(),
            "data": payload,
            "metadata": self.metadata,
            "warnings": list(self.warnings),
            "occurred_at": self.occurred_at.isoformat(),
            "duration_ms": self.duration_ms,
            "error": (self.error.to_dict() if self.error is not None else None),
        }

    def __bool__(
        self,
    ) -> bool:
        """
        Truthiness follows workflow success.
        """

        return self.success

    def __str__(
        self,
    ) -> str:
        """
        Human-readable representation.
        """

        if self.message:
            return self.message

        return (
            "Workflow completed successfully."
            if self.success
            else "Workflow execution failed."
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer-friendly representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"success={self.success!r}, "
            f"code={self.code!r}, "
            f"context={self.context.workflow_name!r}, "
            f"occurred_at={self.occurred_at.isoformat()!r}"
            ")"
        )


__all__: tuple[str, ...] = ("WorkflowResult",)
