"""
Messaging exceptions.
"""

from __future__ import annotations


class MessagingError(Exception):
    """Base messaging error."""


class MessagePublishError(MessagingError):
    """Message publishing failed."""


class MessageRoutingError(MessagingError):
    """Message routing failed."""


class MessageQueueError(MessagingError):
    """Queue operation failed."""


class MessageDeliveryError(MessagingError):
    """Message delivery failed."""


class MessageHandlerError(MessagingError):
    """Message handler execution failed."""


class SubscriberError(MessagingError):
    """Subscriber operation failed."""


class BusError(MessagingError):
    """Message bus failure."""


__all__ = [
    "MessagingError",
    "MessagePublishError",
    "MessageRoutingError",
    "MessageQueueError",
    "MessageDeliveryError",
    "MessageHandlerError",
    "SubscriberError",
    "BusError",
]
