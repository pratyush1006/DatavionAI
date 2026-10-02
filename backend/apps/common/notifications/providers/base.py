"""
Base notification provider.

DatavionOS
----------

Defines the infrastructure-level provider contract used by
notification delivery channels.

Providers consume the canonical framework notification model
from ``apps.common.notifications.models``.
"""

from __future__ import annotations

from abc import ABC, abstractmethod

from apps.common.notifications.models import Notification


class BaseNotificationProvider(ABC):
    """
    Abstract notification provider.

    Providers are infrastructure adapters responsible for
    delivering notifications through an external or local
    delivery mechanism.

    They must not contain business logic.
    """

    @abstractmethod
    def send(
        self,
        *,
        notification: Notification,
    ) -> bool:
        """
        Deliver a notification.

        Args:
            notification:
                Canonical DatavionOS notification request.

        Returns:
            ``True`` when delivery was accepted successfully.

        Raises:
            Exception:
                Provider-specific delivery failures should propagate
                to the notification channel/dispatcher.
        """

        raise NotImplementedError
