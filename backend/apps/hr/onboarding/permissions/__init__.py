"""
Onboarding permission classes.
"""

from .lifecycle_process import (
    CanCreateLifecycleProcess,
    CanDeleteLifecycleProcess,
    CanUpdateLifecycleProcess,
    CanViewLifecycleProcess,
)
from .lifecycle_task import (
    CanCreateLifecycleTask,
    CanDeleteLifecycleTask,
    CanUpdateLifecycleTask,
    CanViewLifecycleTask,
)
from .task_template import (
    CanCreateTaskTemplate,
    CanDeleteTaskTemplate,
    CanUpdateTaskTemplate,
    CanViewTaskTemplate,
)

__all__ = [
    "CanViewTaskTemplate",
    "CanCreateTaskTemplate",
    "CanUpdateTaskTemplate",
    "CanDeleteTaskTemplate",
    "CanViewLifecycleProcess",
    "CanCreateLifecycleProcess",
    "CanUpdateLifecycleProcess",
    "CanDeleteLifecycleProcess",
    "CanViewLifecycleTask",
    "CanCreateLifecycleTask",
    "CanUpdateLifecycleTask",
    "CanDeleteLifecycleTask",
]
