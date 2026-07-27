"""
Workflow constants for DatavionOS.

Defines framework-wide constants for workflow lifecycle,
state management, and execution behaviour.
"""

from __future__ import annotations

###############################################################################
# Workflow Execution Status
###############################################################################

WORKFLOW_PENDING = "pending"

WORKFLOW_RUNNING = "running"

WORKFLOW_COMPLETED = "completed"

WORKFLOW_FAILED = "failed"

WORKFLOW_CANCELLED = "cancelled"

WORKFLOW_PAUSED = "paused"


###############################################################################
# Workflow State Types
###############################################################################

STATE_INITIAL = "initial"

STATE_NORMAL = "normal"

STATE_FINAL = "final"

STATE_ERROR = "error"


###############################################################################
# Transition Types
###############################################################################

TRANSITION_AUTOMATIC = "automatic"

TRANSITION_MANUAL = "manual"

TRANSITION_EVENT = "event"


###############################################################################
# Default Values
###############################################################################

DEFAULT_WORKFLOW_STATUS = WORKFLOW_PENDING

DEFAULT_STATE_TYPE = STATE_NORMAL


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "DEFAULT_STATE_TYPE",
    "DEFAULT_WORKFLOW_STATUS",
    "STATE_ERROR",
    "STATE_FINAL",
    "STATE_INITIAL",
    "STATE_NORMAL",
    "TRANSITION_AUTOMATIC",
    "TRANSITION_EVENT",
    "TRANSITION_MANUAL",
    "WORKFLOW_CANCELLED",
    "WORKFLOW_COMPLETED",
    "WORKFLOW_FAILED",
    "WORKFLOW_PAUSED",
    "WORKFLOW_PENDING",
    "WORKFLOW_RUNNING",
)
