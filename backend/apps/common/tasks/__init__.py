"""
DatavionOS task framework.

Provides the public API for platform task execution.

Supports:

- Task definitions
- Task registration
- Task execution
- Scheduling contracts
- Scheduler adapters
- Retry configuration
- Queue abstraction

Business applications should import task utilities from this
package instead of internal modules.
"""

from __future__ import annotations

from .adapters import (
    APSchedulerAdapter,
    BaseSchedulerAdapter,
    CeleryBeatAdapter,
    CloudSchedulerAdapter,
    KubernetesCronJobAdapter,
)
from .base import (
    BaseTask,
    TaskContext,
)
from .config import (
    DEFAULT_SCHEDULER_CONFIGURATION,
    DEFAULT_TASK_CONFIGURATION,
    SchedulerConfiguration,
    TaskConfiguration,
)
from .constants import (
    AI_QUEUE,
    AUDIT_QUEUE,
    DEFAULT_MAX_RETRIES,
    DEFAULT_QUEUE,
    DEFAULT_RETRY_DELAY,
    DEFAULT_TASK_TIMEOUT,
    DOCUMENT_QUEUE,
    HIGH_PRIORITY_QUEUE,
    LOW_PRIORITY_QUEUE,
    NOTIFICATION_QUEUE,
    REPORT_QUEUE,
    SEARCH_QUEUE,
    TASK_CANCELLED,
    TASK_COMPLETED,
    TASK_FAILED,
    TASK_PENDING,
    TASK_RUNNING,
    WORKFLOW_QUEUE,
)
from .exceptions import (
    TaskAlreadyRegisteredError,
    TaskBackendError,
    TaskCancelledError,
    TaskConfigurationError,
    TaskError,
    TaskExecutionError,
    TaskNotRegisteredError,
    TaskPayloadError,
    TaskRegistrationError,
    TaskRetryError,
    TaskTimeoutError,
)
from .queues import (
    AI_TASK_QUEUE,
    AUDIT_TASK_QUEUE,
    DEFAULT_TASK_QUEUE,
    DOCUMENT_TASK_QUEUE,
    NOTIFICATION_TASK_QUEUE,
    REPORT_TASK_QUEUE,
    SEARCH_TASK_QUEUE,
    WORKFLOW_TASK_QUEUE,
    TaskQueue,
    get_queue,
)
from .registry import (
    TaskRegistry,
    task_registry,
)
from .runner import (
    TaskRunner,
    execute_task,
    task_runner,
)
from .scheduler import (
    ScheduleDefinition,
    TaskScheduler,
    task_scheduler,
)
from .types import (
    TaskCallable,
    TaskID,
    TaskName,
    TaskPayload,
    TaskResult,
    TaskStatus,
)

__all__: tuple[str, ...] = (
    # Base
    "BaseTask",
    "TaskContext",
    # Configuration
    "TaskConfiguration",
    "SchedulerConfiguration",
    "DEFAULT_TASK_CONFIGURATION",
    "DEFAULT_SCHEDULER_CONFIGURATION",
    # Registry
    "TaskRegistry",
    "task_registry",
    # Runner
    "TaskRunner",
    "task_runner",
    "execute_task",
    # Scheduler
    "ScheduleDefinition",
    "TaskScheduler",
    "task_scheduler",
    # Scheduler Adapters
    "BaseSchedulerAdapter",
    "CeleryBeatAdapter",
    "APSchedulerAdapter",
    "CloudSchedulerAdapter",
    "KubernetesCronJobAdapter",
    # Queue Abstraction
    "TaskQueue",
    "get_queue",
    "DEFAULT_TASK_QUEUE",
    "AI_TASK_QUEUE",
    "DOCUMENT_TASK_QUEUE",
    "NOTIFICATION_TASK_QUEUE",
    "SEARCH_TASK_QUEUE",
    "AUDIT_TASK_QUEUE",
    "WORKFLOW_TASK_QUEUE",
    "REPORT_TASK_QUEUE",
    # Types
    "TaskCallable",
    "TaskID",
    "TaskName",
    "TaskPayload",
    "TaskResult",
    "TaskStatus",
    # Task States
    "TASK_PENDING",
    "TASK_RUNNING",
    "TASK_COMPLETED",
    "TASK_FAILED",
    "TASK_CANCELLED",
    # Configuration Defaults
    "DEFAULT_TASK_TIMEOUT",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_RETRY_DELAY",
    # Queue Constants
    "DEFAULT_QUEUE",
    "HIGH_PRIORITY_QUEUE",
    "LOW_PRIORITY_QUEUE",
    "AI_QUEUE",
    "DOCUMENT_QUEUE",
    "NOTIFICATION_QUEUE",
    "SEARCH_QUEUE",
    "AUDIT_QUEUE",
    "WORKFLOW_QUEUE",
    "REPORT_QUEUE",
    # Exceptions
    "TaskError",
    "TaskConfigurationError",
    "TaskPayloadError",
    "TaskRegistrationError",
    "TaskAlreadyRegisteredError",
    "TaskNotRegisteredError",
    "TaskExecutionError",
    "TaskBackendError",
    "TaskTimeoutError",
    "TaskRetryError",
    "TaskCancelledError",
)
