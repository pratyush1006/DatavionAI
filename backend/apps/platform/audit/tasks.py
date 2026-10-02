"""
Celery tasks for the Audit application.
"""

from __future__ import annotations

from celery import shared_task

from apps.platform.audit.dispatch import (
    dispatch_audit_event,
)


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    retry_backoff=True,
    retry_jitter=True,
    retry_kwargs={
        "max_retries": 5,
    },
)
def create_audit_log(
    self,
    **kwargs,
):
    """
    Create an audit log asynchronously.
    """

    dispatch_audit_event(
        **kwargs,
    )
