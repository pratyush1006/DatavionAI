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
    TypeAlias,
)

###############################################################################
# Workflow Identity
###############################################################################

WorkflowName: TypeAlias = str

WorkflowID: TypeAlias = str


###############################################################################
# Workflow State
###############################################################################

StateName: TypeAlias = str


TransitionName: TypeAlias = str


###############################################################################
# Workflow Context
###############################################################################

WorkflowContext: TypeAlias = Mapping[
    str,
    Any,
]


MutableWorkflowContext: TypeAlias = dict[
    str,
    Any,
]


###############################################################################
# Workflow Execution
###############################################################################

WorkflowResult: TypeAlias = Any


TransitionCondition: TypeAlias = Callable[
    [
        WorkflowContext,
    ],
    bool,
]


TransitionAction: TypeAlias = Callable[
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
