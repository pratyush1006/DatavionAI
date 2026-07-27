"""
Workflow configuration models for DatavionOS.

Provides immutable configuration objects used by the workflow
framework.

The configuration layer controls workflow execution behaviour
without coupling to business applications.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.common.workflow.constants import (
    DEFAULT_WORKFLOW_STATUS,
)
from apps.common.workflow.types import (
    WorkflowName,
)


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowConfiguration:
    """
    Workflow definition configuration.

    Represents framework-level workflow settings.
    """

    name: WorkflowName

    description: str = ""

    initial_status: str = DEFAULT_WORKFLOW_STATUS

    max_execution_time: int = 3600

    allow_parallel_execution: bool = False

    audit_enabled: bool = True

    event_notifications_enabled: bool = True


@dataclass(
    frozen=True,
    slots=True,
)
class WorkflowEngineConfiguration:
    """
    Runtime workflow engine configuration.
    """

    max_retries: int = 3

    retry_delay_seconds: int = 5

    enable_async_execution: bool = True

    fail_fast: bool = False

    tenant_isolation: bool = True


DEFAULT_WORKFLOW_ENGINE_CONFIGURATION = WorkflowEngineConfiguration()


__all__: tuple[str, ...] = (
    "DEFAULT_WORKFLOW_ENGINE_CONFIGURATION",
    "WorkflowConfiguration",
    "WorkflowEngineConfiguration",
)
