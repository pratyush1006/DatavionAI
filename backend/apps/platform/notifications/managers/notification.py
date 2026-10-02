"""
Notification manager.

Provides the default manager for Notification and exposes all
custom queryset methods defined in NotificationQuerySet.
"""

from __future__ import annotations

from django.db import models

from apps.platform.notifications.querysets import (
    NotificationQuerySet,
)


class NotificationManager(
    models.Manager.from_queryset(
        NotificationQuerySet,
    ),
):
    """
    Manager for Notification.

    Exposes all NotificationQuerySet methods through
    Notification.objects.
    """

    use_in_migrations = True


__all__ = [
    "NotificationManager",
]
