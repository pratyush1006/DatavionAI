"""
DatavionAI Core Event Framework.

Public exports for the domain event system.
"""

from __future__ import annotations

from apps.core.events.base import DomainEvent
from apps.core.events.dispatcher import EventDispatcher, dispatcher
from apps.core.events.exceptions import (
    EventDispatchError,
    EventError,
    EventRegistrationError,
    HandlerExecutionError,
)
from apps.core.events.handlers import (
    AsyncEventHandler,
    EventHandler,
)
from apps.core.events.publisher import (
    EventPublisher,
    publish_after_commit,
    publish_many_after_commit,
    publisher,
)
from apps.core.events.registry import EventRegistry, registry

__all__: tuple[str, ...] = (
    "AsyncEventHandler",
    "DomainEvent",
    "EventDispatchError",
    "EventDispatcher",
    "EventError",
    "EventHandler",
    "EventPublisher",
    "EventRegistrationError",
    "EventRegistry",
    "HandlerExecutionError",
    "dispatcher",
    "publish_after_commit",
    "publish_many_after_commit",
    "publisher",
    "registry",
)
