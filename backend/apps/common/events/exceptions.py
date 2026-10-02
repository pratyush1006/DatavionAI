"""
Event exception hierarchy for DatavionOS.

Provides reusable exceptions for the platform event framework.
"""

from __future__ import annotations


class EventError(
    Exception,
):
    """
    Base exception for all event-related errors.
    """


class EventRegistrationError(
    EventError,
):
    """
    Raised when event registration fails.
    """


class EventAlreadyRegisteredError(
    EventRegistrationError,
):
    """
    Raised when an event handler is registered more than once.
    """


class EventNotRegisteredError(
    EventRegistrationError,
):
    """
    Raised when an event has no registration.
    """


class EventDispatchError(
    EventError,
):
    """
    Raised when event dispatching fails.
    """


class EventHandlerError(
    EventDispatchError,
):
    """
    Raised when an event handler execution fails.
    """


__all__: tuple[str, ...] = (
    "EventAlreadyRegisteredError",
    "EventDispatchError",
    "EventError",
    "EventHandlerError",
    "EventNotRegisteredError",
    "EventRegistrationError",
)
