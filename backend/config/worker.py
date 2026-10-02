from __future__ import annotations

import os

CELERY_WORKER_HARD_TIME_LIMIT = int(
    os.environ.get("CELERY_WORKER_HARD_TIME_LIMIT", "120")
)
CELERY_WORKER_SOFT_TIME_LIMIT = int(
    os.environ.get("CELERY_WORKER_SOFT_TIME_LIMIT", "90")
)
CELERY_WORKER_MAX_TASKS_PER_CHILD = int(
    os.environ.get("CELERY_WORKER_MAX_TASKS_PER_CHILD", "1000")
)
CELERY_WORKER_PREFETCH_MULTIPLIER = int(
    os.environ.get("CELERY_WORKER_PREFETCH_MULTIPLIER", "1")
)
CELERY_TASK_ACKS_LATE = os.environ.get("CELERY_TASK_ACKS_LATE", "true").lower() in {
    "1",
    "true",
    "yes",
    "on",
}
CELERY_TASK_REJECT_ON_WORKER_LOST = os.environ.get(
    "CELERY_TASK_REJECT_ON_WORKER_LOST", "true"
).lower() in {"1", "true", "yes", "on"}
