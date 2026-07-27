"""
Workflow execution context.

Provides a standardized execution context for all workflows across the
DatavionAI platform.

The context carries identity, tracing, tenancy, and metadata information
throughout workflow execution, enabling consistent logging, auditing,
event correlation, and distributed tracing.
"""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Any
from uuid import UUID, uuid4


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class WorkflowContext:
    """
    Immutable workflow execution context.

    A single WorkflowContext should accompany every workflow execution.

    Attributes
    ----------
    tenant_id:
        Current tenant identifier.

    actor_id:
        User or system performing the operation.

    correlation_id:
        Correlates multiple operations belonging to one request.

    causation_id:
        Event or workflow that triggered this workflow.

    request_id:
        HTTP/API request identifier.

    workflow_name:
        Name of the executing workflow.

    metadata:
        Additional contextual information.
    """

    tenant_id: UUID

    actor_id: UUID

    correlation_id: UUID = field(
        default_factory=uuid4,
    )

    causation_id: UUID | None = None

    request_id: str | None = None

    workflow_name: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    def with_workflow(
        self,
        workflow_name: str,
    ) -> WorkflowContext:
        """
        Return a new context with an updated workflow name.
        """

        return replace(
            self,
            workflow_name=workflow_name,
        )

    def with_request_id(
        self,
        request_id: str,
    ) -> WorkflowContext:
        """
        Return a new context with a request identifier.
        """

        return replace(
            self,
            request_id=request_id,
        )

    def with_actor(
        self,
        actor_id: UUID,
    ) -> WorkflowContext:
        """
        Return a new context for another actor.
        """

        return replace(
            self,
            actor_id=actor_id,
        )

    def with_metadata(
        self,
        **metadata: Any,
    ) -> WorkflowContext:
        """
        Return a new context with additional metadata.

        Existing metadata is preserved unless overwritten by the
        supplied values.
        """

        return replace(
            self,
            metadata={
                **self.metadata,
                **metadata,
            },
        )

    def merge_metadata(
        self,
        metadata: dict[str, Any],
    ) -> WorkflowContext:
        """
        Merge a metadata dictionary into the current context.
        """

        return replace(
            self,
            metadata={
                **self.metadata,
                **metadata,
            },
        )

    def child_context(
        self,
        *,
        workflow_name: str | None = None,
        causation_id: UUID | None = None,
    ) -> WorkflowContext:
        """
        Create a child workflow context.

        The child inherits:

        - tenant_id
        - actor_id
        - request_id
        - correlation_id

        A new workflow name may be assigned while preserving
        distributed tracing.
        """

        return WorkflowContext(
            tenant_id=self.tenant_id,
            actor_id=self.actor_id,
            correlation_id=self.correlation_id,
            causation_id=causation_id,
            request_id=self.request_id,
            workflow_name=workflow_name,
            metadata=self.metadata.copy(),
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize the workflow context.

        Useful for:

        - structured logging
        - audit records
        - event metadata
        - background task payloads
        """

        return {
            "tenant_id": str(self.tenant_id),
            "actor_id": str(self.actor_id),
            "correlation_id": str(self.correlation_id),
            "causation_id": (str(self.causation_id) if self.causation_id else None),
            "request_id": self.request_id,
            "workflow_name": self.workflow_name,
            "metadata": self.metadata,
        }

    @property
    def has_request_id(
        self,
    ) -> bool:
        """
        Whether the workflow has an associated request.
        """

        return self.request_id is not None

    @property
    def is_root(
        self,
    ) -> bool:
        """
        Whether this is the root workflow.

        Root workflows have no causation identifier.
        """

        return self.causation_id is None

    @property
    def is_child(
        self,
    ) -> bool:
        """
        Whether this workflow was triggered by another workflow.
        """

        return self.causation_id is not None

    @classmethod
    def create(
        cls,
        *,
        tenant_id: UUID,
        actor_id: UUID,
        workflow_name: str,
        request_id: str | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> WorkflowContext:
        """
        Create a new root workflow context.

        A new correlation identifier is generated automatically.
        """

        return cls(
            tenant_id=tenant_id,
            actor_id=actor_id,
            workflow_name=workflow_name,
            request_id=request_id,
            metadata=metadata or {},
        )

    @classmethod
    def system(
        cls,
        *,
        tenant_id: UUID,
        workflow_name: str,
        metadata: dict[str, Any] | None = None,
    ) -> WorkflowContext:
        """
        Create a workflow context for a system-initiated operation.

        Intended for scheduled jobs, maintenance tasks, and background
        workflows that are not initiated by an end user.
        """

        return cls(
            tenant_id=tenant_id,
            actor_id=UUID(int=0),
            workflow_name=workflow_name,
            metadata=metadata or {},
        )

    def __repr__(self) -> str:
        """
        Developer-friendly representation.
        """

        return (
            "WorkflowContext("
            f"tenant_id={self.tenant_id!s}, "
            f"actor_id={self.actor_id!s}, "
            f"workflow_name={self.workflow_name!r}, "
            f"correlation_id={self.correlation_id!s}"
            ")"
        )


__all__: tuple[str, ...] = ("WorkflowContext",)
