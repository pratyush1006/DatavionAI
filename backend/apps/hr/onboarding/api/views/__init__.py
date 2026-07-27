"""
Onboarding API views.
"""

from .lifecycle_process import (
    LifecycleProcessListCreateAPIView,
    LifecycleProcessRetrieveUpdateDestroyAPIView,
)
from .lifecycle_task import (
    LifecycleTaskListCreateAPIView,
    LifecycleTaskRetrieveUpdateDestroyAPIView,
)
from .task_template import (
    LifecycleTaskTemplateListCreateAPIView,
    LifecycleTaskTemplateRetrieveUpdateDestroyAPIView,
)
from .workflow import (
    LifecycleProcessCancelAPIView,
    LifecycleProcessCompleteAPIView,
)

__all__ = [
    "LifecycleTaskTemplateListCreateAPIView",
    "LifecycleTaskTemplateRetrieveUpdateDestroyAPIView",
    "LifecycleProcessListCreateAPIView",
    "LifecycleProcessRetrieveUpdateDestroyAPIView",
    "LifecycleTaskListCreateAPIView",
    "LifecycleTaskRetrieveUpdateDestroyAPIView",
    "LifecycleProcessCompleteAPIView",
    "LifecycleProcessCancelAPIView",
]
