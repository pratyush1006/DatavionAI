"""
DatavionOS workflow framework.

Provides the public API for platform workflow capabilities.

Supports:

- Workflow definitions
- Workflow states
- State transitions
- Workflow execution
- Runtime orchestration
- Registry-based discovery

Business applications should import workflow utilities from
this package instead of internal modules.
"""

from __future__ import annotations

from .config import (
    DEFAULT_WORKFLOW_ENGINE_CONFIGURATION,
    WorkflowConfiguration,
    WorkflowEngineConfiguration,
)
from .constants import (
    DEFAULT_STATE_TYPE,
    DEFAULT_WORKFLOW_STATUS,
    STATE_ERROR,
    STATE_FINAL,
    STATE_INITIAL,
    STATE_NORMAL,
    TRANSITION_AUTOMATIC,
    TRANSITION_EVENT,
    TRANSITION_MANUAL,
    WORKFLOW_CANCELLED,
    WORKFLOW_COMPLETED,
    WORKFLOW_FAILED,
    WORKFLOW_PAUSED,
    WORKFLOW_PENDING,
    WORKFLOW_RUNNING,
)
from .engine import (
    WorkflowEngine,
    workflow_engine,
)
from .exceptions import (
    InvalidTransitionError,
    WorkflowAlreadyRegisteredError,
    WorkflowConfigurationError,
    WorkflowContextError,
    WorkflowError,
    WorkflowExecutionError,
    WorkflowNotFoundError,
    WorkflowRegistrationError,
    WorkflowStateError,
    WorkflowTimeoutError,
)
from .models import (
    Workflow,
    WorkflowExecution,
    WorkflowExecutionResult,
    WorkflowState,
    WorkflowTransition,
)
from .registry import (
    WorkflowRegistry,
    workflow_registry,
)
from .services import (
    WorkflowService,
    workflow_service,
)
from .types import (
    MutableWorkflowContext,
    StateName,
    TransitionAction,
    TransitionCondition,
    TransitionName,
    WorkflowContext,
    WorkflowID,
    WorkflowName,
    WorkflowResult,
)

__all__: tuple[str, ...] = (
    # Models
    "Workflow",
    "WorkflowState",
    "WorkflowTransition",
    "WorkflowExecution",
    "WorkflowExecutionResult",
    # Services
    "WorkflowService",
    "workflow_service",
    # Registry
    "WorkflowRegistry",
    "workflow_registry",
    # Engine
    "WorkflowEngine",
    "workflow_engine",
    # Configuration
    "WorkflowConfiguration",
    "WorkflowEngineConfiguration",
    "DEFAULT_WORKFLOW_ENGINE_CONFIGURATION",
    # Types
    "WorkflowName",
    "WorkflowID",
    "WorkflowContext",
    "MutableWorkflowContext",
    "WorkflowResult",
    "StateName",
    "TransitionName",
    "TransitionCondition",
    "TransitionAction",
    # Constants
    "WORKFLOW_PENDING",
    "WORKFLOW_RUNNING",
    "WORKFLOW_COMPLETED",
    "WORKFLOW_FAILED",
    "WORKFLOW_CANCELLED",
    "WORKFLOW_PAUSED",
    "STATE_INITIAL",
    "STATE_NORMAL",
    "STATE_FINAL",
    "STATE_ERROR",
    "TRANSITION_AUTOMATIC",
    "TRANSITION_MANUAL",
    "TRANSITION_EVENT",
    "DEFAULT_WORKFLOW_STATUS",
    "DEFAULT_STATE_TYPE",
    # Exceptions
    "WorkflowError",
    "WorkflowConfigurationError",
    "WorkflowNotFoundError",
    "WorkflowAlreadyRegisteredError",
    "WorkflowRegistrationError",
    "WorkflowStateError",
    "InvalidTransitionError",
    "WorkflowExecutionError",
    "WorkflowContextError",
    "WorkflowTimeoutError",
)
