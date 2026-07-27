"""
Task type definitions for DatavionOS.

Provides reusable type contracts for the task framework.

These types are framework-level only and remain independent
from Celery, Redis, RQ, or any queue implementation.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any, TypeAlias

###############################################################################
# Task Identity
###############################################################################

TaskName: TypeAlias = str

TaskID: TypeAlias = str


###############################################################################
# Task Payload
###############################################################################

TaskPayload: TypeAlias = dict[
    str,
    Any,
]


###############################################################################
# Task Result
###############################################################################

TaskResult: TypeAlias = dict[
    str,
    Any,
]


###############################################################################
# Task Function
###############################################################################

TaskCallable: TypeAlias = Callable[
    [
        TaskPayload,
    ],
    TaskResult,
]


###############################################################################
# Task Status
###############################################################################

TaskStatus: TypeAlias = str


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
