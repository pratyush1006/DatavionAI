"""
Task type definitions for DatavionOS.

Provides reusable type contracts for the task framework.

These types are framework-level only and remain independent
from Celery, Redis, RQ, or any queue implementation.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

###############################################################################
# Task Identity
###############################################################################

type TaskName = str

type TaskID = str


###############################################################################
# Task Payload
###############################################################################

type TaskPayload = dict[
    str,
    Any,
]


###############################################################################
# Task Result
###############################################################################

type TaskResult = dict[
    str,
    Any,
]


###############################################################################
# Task Function
###############################################################################

type TaskCallable = Callable[
    [
        TaskPayload,
    ],
    TaskResult,
]


###############################################################################
# Task Status
###############################################################################

type TaskStatus = str


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "TaskCallable",
    "TaskID",
    "TaskName",
    "TaskPayload",
    "TaskResult",
    "TaskStatus",
)
