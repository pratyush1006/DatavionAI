"""
Celery tasks for the Notifications application.
"""

from __future__ import annotations

from celery import shared_task

from apps.platform.notifications.models import Notification
from apps.platform.notifications.services.notification import (
    NotificationService,
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
def send_notification(
    self,
    notification_id: str,
) -> None:
    """
    Deliver a notification asynchronously.
    """

    notification = Notification.objects.filter(
        pk=notification_id,
    ).first()

    if notification is None:
        return

    NotificationService._deliver(
        notification=notification,
    )


__all__ = [
    "send_notification",
]
