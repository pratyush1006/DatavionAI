"""
Celery application configuration.

This module initializes the global Celery application used
throughout the DatavionAI platform.
"""

from __future__ import annotations

import os

from celery import Celery

# --------------------------------------------------------------------------
# Django Settings
# --------------------------------------------------------------------------

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings",
)

# --------------------------------------------------------------------------
# Celery Application
# --------------------------------------------------------------------------

app = Celery(
    "datavion",
)

# --------------------------------------------------------------------------
# Load configuration from Django settings
# --------------------------------------------------------------------------

app.config_from_object(
    "django.conf:settings",
    namespace="CELERY",
)

# --------------------------------------------------------------------------
# Auto-discover tasks
# --------------------------------------------------------------------------

app.autodiscover_tasks()

# --------------------------------------------------------------------------
# Debug Task
# --------------------------------------------------------------------------


@app.task(bind=True)
def debug_task(
    self,
):
    """
    Debug Celery task.

    Useful for verifying worker connectivity.
    """

    print(
        f"Request: {self.request!r}",
    )


__all__ = [
    "app",
]
