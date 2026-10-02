"""
Celery system checks for the DatavionOS platform.

Validates asynchronous task processing configuration.
"""

from __future__ import annotations

from django.conf import settings
from django.core.checks import Tags, Warning, register


@register(Tags.compatibility)
def celery_check(
    app_configs,
    **kwargs,
):
    """
    Validate Celery configuration.
    """

    messages = []

    broker_url = getattr(
        settings,
        "CELERY_BROKER_URL",
        None,
    )

    if not broker_url:
        messages.append(
            Warning(
                "CELERY_BROKER_URL is not configured.",
                hint=("Configure Celery broker URL for background task processing."),
                id="datavion.W006",
            )
        )

    result_backend = getattr(
        settings,
        "CELERY_RESULT_BACKEND",
        None,
    )

    if not result_backend:
        messages.append(
            Warning(
                "CELERY_RESULT_BACKEND is not configured.",
                hint=("Configure Celery result backend for task monitoring."),
                id="datavion.W011",
            )
        )

    return messages


__all__ = [
    "celery_check",
]
