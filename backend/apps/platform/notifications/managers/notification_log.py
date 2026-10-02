"""
Notification log manager.

Provides the default manager for NotificationLog and exposes all
custom queryset methods defined in NotificationLogQuerySet.
"""

from __future__ import annotations

from django.db import models

from apps.platform.notifications.querysets import (
    NotificationLogQuerySet,
)


class NotificationLogManager(
    models.Manager.from_queryset(
        NotificationLogQuerySet,
    ),
):
    """
    Manager for NotificationLog.

    Exposes all NotificationLogQuerySet methods through
    NotificationLog.objects.
    """

    use_in_migrations = True


__all__ = [
    "NotificationLogManager",
]
