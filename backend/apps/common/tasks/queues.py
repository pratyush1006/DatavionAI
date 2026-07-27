"""
Task queue abstraction for DatavionOS.

Provides queue definitions and routing capabilities.

This module is infrastructure independent.

Supported backends:

- Celery
- Redis Queue
- RabbitMQ
- AWS SQS
- Azure Service Bus

The task framework only knows queue contracts.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
)

from apps.common.tasks.constants import (
    AI_QUEUE,
    AUDIT_QUEUE,
    DEFAULT_QUEUE,
    DOCUMENT_QUEUE,
    NOTIFICATION_QUEUE,
    REPORT_QUEUE,
    SEARCH_QUEUE,
    WORKFLOW_QUEUE,
)


@dataclass(
    frozen=True,
    slots=True,
)
class TaskQueue:
    """
    Represents a task execution queue.

    Queues allow workload isolation:

    - AI processing
    - Documents
    - Notifications
    - Search indexing
    - Audit processing
    - Reports
    """

    name: str

    description: str = ""


DEFAULT_TASK_QUEUE = TaskQueue(
    name=DEFAULT_QUEUE,
    description="General background tasks.",
)


AI_TASK_QUEUE = TaskQueue(
    name=AI_QUEUE,
    description="AI and ML processing tasks.",
)


DOCUMENT_TASK_QUEUE = TaskQueue(
    name=DOCUMENT_QUEUE,
    description="Document processing and extraction tasks.",
)


NOTIFICATION_TASK_QUEUE = TaskQueue(
    name=NOTIFICATION_QUEUE,
    description="Email, SMS and push notification tasks.",
)


SEARCH_TASK_QUEUE = TaskQueue(
    name=SEARCH_QUEUE,
    description="Search indexing and retrieval tasks.",
)


AUDIT_TASK_QUEUE = TaskQueue(
    name=AUDIT_QUEUE,
    description="Audit and compliance processing tasks.",
)


WORKFLOW_TASK_QUEUE = TaskQueue(
    name=WORKFLOW_QUEUE,
    description="Workflow automation tasks.",
)


REPORT_TASK_QUEUE = TaskQueue(
    name=REPORT_QUEUE,
    description="Analytics and reporting tasks.",
)


QUEUE_REGISTRY: dict[
    str,
    TaskQueue,
] = {
    queue.name: queue
    for queue in (
        DEFAULT_TASK_QUEUE,
        AI_TASK_QUEUE,
        DOCUMENT_TASK_QUEUE,
        NOTIFICATION_TASK_QUEUE,
        SEARCH_TASK_QUEUE,
        AUDIT_TASK_QUEUE,
        WORKFLOW_TASK_QUEUE,
        REPORT_TASK_QUEUE,
    )
}


def get_queue(
    name: str,
) -> TaskQueue:
    """
    Resolve queue by name.

    Falls back to default queue.
    """

    return QUEUE_REGISTRY.get(
        name,
        DEFAULT_TASK_QUEUE,
    )


__all__: tuple[str, ...] = (
    "AI_TASK_QUEUE",
    "AUDIT_TASK_QUEUE",
    "DEFAULT_TASK_QUEUE",
    "DOCUMENT_TASK_QUEUE",
    "NOTIFICATION_TASK_QUEUE",
    "QUEUE_REGISTRY",
    "REPORT_TASK_QUEUE",
    "SEARCH_TASK_QUEUE",
    "TaskQueue",
    "WORKFLOW_TASK_QUEUE",
    "get_queue",
)
