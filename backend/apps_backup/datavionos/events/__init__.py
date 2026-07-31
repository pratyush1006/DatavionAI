"""
DatavionOS Event Processing Framework.

Enterprise Event-Driven Architecture (EDA) infrastructure.

This package provides:

- Domain Events
- Integration Events
- Event Bus
- Event Handlers
- Event Middleware
- Event Context
- Event Store
- Event Publisher
- Event Subscriber
- Event Results
- Strongly Typed Exceptions

This package forms the event-driven foundation
of DatavionOS.
"""

from __future__ import annotations

from apps.datavionos.events.bus import (
    EventBus,
)
from apps.datavionos.events.context import (
    EventContext,
)
from apps.datavionos.events.dispatcher import (
    EventDispatcher,
)
from apps.datavionos.events.event import (
    Event,
)
from apps.datavionos.events.exceptions import (
    DeadLetterQueueException,
    DuplicateEventHandlerException,
    EventConcurrencyException,
    EventDeserializationException,
    EventDispatchException,
    EventException,
    EventHandlerNotFoundException,
    EventMiddlewareException,
    EventPublicationException,
    EventPublisherException,
    EventReplayException,
    EventSerializationException,
    EventStoreException,
    EventSubscriberException,
    EventTransportException,
    EventValidationException,
)
from apps.datavionos.events.handler import (
    EventHandler,
)
from apps.datavionos.events.middleware import (
    EventMiddleware,
)
from apps.datavionos.events.publisher import (
    EventPublisher,
)
from apps.datavionos.events.registry import (
    EventRegistry,
)
from apps.datavionos.events.result import (
    EventResult,
)
from apps.datavionos.events.store import (
    EventStore,
)
from apps.datavionos.events.subscriber import (
    EventSubscriber,
)

__all__ = [
    # Core
    "Event",
    "EventHandler",
    "EventDispatcher",
    "EventRegistry",
    "EventBus",
    "EventMiddleware",
    "EventContext",
    "EventResult",
    # Infrastructure
    "EventPublisher",
    "EventSubscriber",
    "EventStore",
    # Exceptions
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
