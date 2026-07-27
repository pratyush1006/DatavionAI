"""
DatavionOS task scheduler adapters.

Provides scheduler integration contracts for:

- Celery Beat
- APScheduler
- Cloud Scheduler
- Kubernetes CronJobs

Adapters are intentionally isolated from external
dependencies. Deployment layers provide the actual
scheduler implementations.
"""

from __future__ import annotations

from .apscheduler import (
    APSchedulerAdapter,
)
from .base import (
    BaseSchedulerAdapter,
)
from .celery_beat import (
    CeleryBeatAdapter,
)
from .cloud_scheduler import (
    CloudSchedulerAdapter,
)
from .kubernetes_cron import (
    KubernetesCronJobAdapter,
)

__all__: tuple[str, ...] = (
    "BaseSchedulerAdapter",
    "CeleryBeatAdapter",
    "APSchedulerAdapter",
    "CloudSchedulerAdapter",
    "KubernetesCronJobAdapter",
)
