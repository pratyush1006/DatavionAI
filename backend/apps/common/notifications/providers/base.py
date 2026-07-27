"""
Base notification provider.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)

from apps.platform.notifications.models import Notification


class BaseNotificationProvider(
    ABC,
):
    """
    Abstract notification provider.

    Every notification provider must implement
    this interface.
    """

    @abstractmethod
    def send(
        self,
        *,
        notification: Notification,
    ) -> bool:
        """
        Send a notification.

        Returns:
            True if delivery succeeded.
        """

        raise NotImplementedError
