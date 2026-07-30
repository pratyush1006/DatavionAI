"""
Workflow type definitions for DatavionOS.

Provides reusable type aliases shared across the workflow
framework.
"""

from __future__ import annotations

from collections.abc import (
    Callable,
    Mapping,
)
from typing import (
    Any,
)

###############################################################################
# Workflow Identity
###############################################################################

type WorkflowName = str

type WorkflowID = str


###############################################################################
# Workflow State
###############################################################################

type StateName = str


type TransitionName = str


###############################################################################
# Workflow Context
###############################################################################

type WorkflowContext = Mapping[
    str,
    Any,
]


type MutableWorkflowContext = dict[
    str,
    Any,
]


###############################################################################
# Workflow Execution
###############################################################################

type WorkflowResult = Any


type TransitionCondition = Callable[
    [
        WorkflowContext,
    ],
    bool,
]


type TransitionAction = Callable[
    [
        WorkflowContext,
    ],
    WorkflowResult,
]


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "MutableWorkflowContext",
    "StateName",
    "TransitionAction",
    "TransitionCondition",
    "TransitionName",
    "WorkflowContext",
    "WorkflowID",
    "WorkflowName",
    "WorkflowResult",
)
