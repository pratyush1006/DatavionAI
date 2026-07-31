"""
DatavionOS Event Exceptions.
"""

from __future__ import annotations

from apps.datavionos.events.event import (
    Event,
)


class EventException(Exception):
    """
    Base exception for all event
    infrastructure.
    """

    def __init__(
        self,
        message: str,
        *,
        event_name: str = "",
    ) -> None:
        super().__init__(
            message,
        )

        self.event_name = event_name


class EventHandlerNotFoundException(
    EventException,
):
    """
    Raised when an event handler
    cannot be found.
    """

    def __init__(
        self,
        event_type: type[Event],
        *,
        handler_name: str = "",
    ) -> None:
        super().__init__(
            (f"No handler found for {event_type.__qualname__}."),
            event_name=event_type.__qualname__,
        )

        self.handler_name = handler_name


class DuplicateEventHandlerException(
    EventException,
):
    """
    Raised when duplicate handlers
    are registered.
    """

    def __init__(
        self,
        event_type: type[Event],
        *,
        handler_name: str,
    ) -> None:
        super().__init__(
            (f"{handler_name} is already registered for {event_type.__qualname__}."),
            event_name=event_type.__qualname__,
        )

        self.handler_name = handler_name


class EventValidationException(
    EventException,
):
    """
    Raised when validation fails.
    """


class EventPublicationException(
    EventException,
):
    """
    Raised when publication fails.
    """


class EventDispatchException(
    EventException,
):
    """
    Raised when dispatch fails.
    """


class EventStoreException(
    EventException,
):
    """
    Raised when the event store
    operation fails.
    """


class EventReplayException(
    EventException,
):
    """
    Raised when replay fails.
    """


class EventConcurrencyException(
    EventException,
):
    """
    Raised when optimistic
    concurrency fails.
    """


class EventSubscriberException(
    EventException,
):
    """
    Raised by subscribers.
    """


class EventPublisherException(
    EventException,
):
    """
    Raised by publishers.
    """


class EventTransportException(
    EventException,
):
    """
    Raised when transport
    communication fails.
    """

    def __init__(
        self,
        transport: str,
        message: str,
        *,
        event_name: str = "",
    ) -> None:
        super().__init__(
            f"[{transport}] {message}",
            event_name=event_name,
        )

        self.transport = transport


class EventSerializationException(
    EventException,
):
    """
    Raised when serialization fails.
    """


class EventDeserializationException(
    EventException,
):
    """
    Raised when deserialization fails.
    """


class EventMiddlewareException(
    EventException,
):
    """
    Raised when middleware fails.
    """

    def __init__(
        self,
        middleware_name: str,
        *,
        event_name: str = "",
        inner_exception: Exception | None = None,
    ) -> None:
        super().__init__(
            (f"Middleware {middleware_name} failed."),
            event_name=event_name,
        )

        self.middleware_name = middleware_name
        self.inner_exception = inner_exception


class DeadLetterQueueException(
    EventException,
):
    """
    Raised when DLQ operations fail.
    """


__all__ = [
    "EventException",
    "EventHandlerNotFoundException",
    "DuplicateEventHandlerException",
    "EventValidationException",
    "EventPublicationException",
    "EventDispatchException",
    "EventStoreException",
    "EventReplayException",
    "EventConcurrencyException",
    "EventSubscriberException",
    "EventPublisherException",
    "EventTransportException",
    "EventSerializationException",
    "EventDeserializationException",
    "EventMiddlewareException",
    "DeadLetterQueueException",
]
