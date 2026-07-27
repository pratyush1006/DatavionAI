"""
Event framework exceptions.
"""

from __future__ import annotations


class EventError(Exception):
    """
    Base event exception.
    """


class EventRegistrationError(EventError):
    """
    Raised when an event handler cannot be registered.
    """


class EventDispatchError(EventError):
    """
    Raised when an event cannot be dispatched.
    """


class HandlerExecutionError(EventDispatchError):
    """
    Raised when an event handler fails.
    """


__all__: tuple[str, ...] = (
    "EventDispatchError",
    "EventError",
    "EventRegistrationError",
    "HandlerExecutionError",
)
