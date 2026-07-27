"""
Notification exception hierarchy for DatavionOS.

Provides reusable exceptions for the notification framework.
"""

from __future__ import annotations


class NotificationError(
    Exception,
):
    """
    Base exception for notification errors.
    """


class NotificationConfigurationError(
    NotificationError,
):
    """
    Raised when notification configuration is invalid.
    """


class NotificationNotFoundError(
    NotificationError,
):
    """
    Raised when a notification definition does not exist.
    """


class NotificationAlreadyRegisteredError(
    NotificationError,
):
    """
    Raised when registering an existing notification.
    """


class NotificationRegistrationError(
    NotificationError,
):
    """
    Raised when notification registration fails.
    """


class NotificationChannelError(
    NotificationError,
):
    """
    Raised when notification channel handling fails.
    """


class NotificationProviderError(
    NotificationChannelError,
):
    """
    Raised when an external provider fails.

    Examples:

    - Email provider failure
    - SMS gateway failure
    - Push provider failure
    """


class NotificationDispatchError(
    NotificationError,
):
    """
    Raised when notification dispatch fails.
    """


class NotificationTemplateError(
    NotificationError,
):
    """
    Raised when notification template processing fails.
    """


class NotificationRecipientError(
    NotificationError,
):
    """
    Raised when recipient validation fails.
    """


__all__: tuple[str, ...] = (
    "NotificationAlreadyRegisteredError",
    "NotificationChannelError",
    "NotificationConfigurationError",
    "NotificationDispatchError",
    "NotificationError",
    "NotificationNotFoundError",
    "NotificationProviderError",
    "NotificationRecipientError",
    "NotificationRegistrationError",
    "NotificationTemplateError",
)
