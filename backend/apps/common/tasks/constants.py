"""
Task framework constants for DatavionOS.

Defines task lifecycle states, retry defaults,
and platform queue names.
"""

from __future__ import annotations

###############################################################################
# Task States
###############################################################################

TASK_PENDING = "pending"

TASK_RUNNING = "running"

TASK_COMPLETED = "completed"

TASK_FAILED = "failed"

TASK_CANCELLED = "cancelled"


###############################################################################
# Default Configuration
###############################################################################

DEFAULT_TASK_TIMEOUT = 300

DEFAULT_MAX_RETRIES = 3

DEFAULT_RETRY_DELAY = 60


###############################################################################
# Queue Names
###############################################################################

DEFAULT_QUEUE = "default"

HIGH_PRIORITY_QUEUE = "high"

LOW_PRIORITY_QUEUE = "low"


# AI Processing

AI_QUEUE = "ai"


# Document Processing

DOCUMENT_QUEUE = "documents"


# Notifications

NOTIFICATION_QUEUE = "notifications"


# Search Indexing

SEARCH_QUEUE = "search"


# Compliance / Audit

AUDIT_QUEUE = "audit"


# Workflow Execution

WORKFLOW_QUEUE = "workflow"


# Reporting / Analytics

REPORT_QUEUE = "reports"


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "AI_QUEUE",
    "AUDIT_QUEUE",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_QUEUE",
    "DEFAULT_RETRY_DELAY",
    "DEFAULT_TASK_TIMEOUT",
    "DOCUMENT_QUEUE",
    "HIGH_PRIORITY_QUEUE",
    "LOW_PRIORITY_QUEUE",
    "NOTIFICATION_QUEUE",
    "REPORT_QUEUE",
    "SEARCH_QUEUE",
    "TASK_CANCELLED",
    "TASK_COMPLETED",
    "TASK_FAILED",
    "TASK_PENDING",
    "TASK_RUNNING",
    "WORKFLOW_QUEUE",
)
