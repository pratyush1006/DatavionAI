"""
DatavionOS event framework.

Provides the public API for the platform event infrastructure.

The event framework supports:

- Event definitions
- Event payloads
- Event handlers
- Handler registration
- Event dispatching
- Audit/workflow/notification integrations

Business applications should import from this package instead
of internal modules.
"""

from __future__ import annotations

from .constants import (
    CORRELATION_ID_FIELD,
    DEFAULT_EVENT_SOURCE,
    DEFAULT_EVENT_VERSION,
    EVENT_CREATED_SUFFIX,
    EVENT_DELETED_SUFFIX,
    EVENT_ID_FIELD,
    EVENT_METADATA_FIELD,
    EVENT_NAME_FIELD,
    EVENT_PAYLOAD_FIELD,
    EVENT_SEPARATOR,
    EVENT_SOURCE_FIELD,
    EVENT_TIMESTAMP_FIELD,
    EVENT_UPDATED_SUFFIX,
    EVENT_VERSION_FIELD,
    ORGANIZATION_ID_FIELD,
    REQUEST_ID_FIELD,
    TENANT_ID_FIELD,
    USER_ID_FIELD,
)
from .dispatcher import (
    EventDispatcher,
    dispatch_event,
    event_dispatcher,
)
from .exceptions import (
    EventAlreadyRegisteredError,
    EventDispatchError,
    EventError,
    EventHandlerError,
    EventNotRegisteredError,
    EventRegistrationError,
)
from .handlers import (
    BaseEventHandler,
    FunctionEventHandler,
)
from .models import (
    Event,
    EventResult,
)
from .payloads import (
    AuditEventPayload,
    BaseEventPayload,
    SystemEventPayload,
    TenantEventPayload,
    UserEventPayload,
)
from .registry import (
    EventRegistry,
    event_registry,
)
from .types import (
    EventCallback,
    EventHandler,
    EventID,
    EventMetadata,
    EventName,
    EventPayload,
)

__all__: tuple[str, ...] = (
    # Models
    "Event",
    "EventResult",
    # Payloads
    "BaseEventPayload",
    "AuditEventPayload",
    "TenantEventPayload",
    "UserEventPayload",
    "SystemEventPayload",
    # Handlers
    "BaseEventHandler",
    "FunctionEventHandler",
    "EventHandler",
    # Dispatcher
    "EventDispatcher",
    "event_dispatcher",
    "dispatch_event",
    # Registry
    "EventRegistry",
    "event_registry",
    # Types
    "EventCallback",
    "EventID",
    "EventMetadata",
    "EventName",
    "EventPayload",
    # Constants
    "EVENT_ID_FIELD",
    "EVENT_NAME_FIELD",
    "EVENT_VERSION_FIELD",
    "EVENT_SOURCE_FIELD",
    "EVENT_TIMESTAMP_FIELD",
    "EVENT_PAYLOAD_FIELD",
    "EVENT_METADATA_FIELD",
    "REQUEST_ID_FIELD",
    "CORRELATION_ID_FIELD",
    "TENANT_ID_FIELD",
    "ORGANIZATION_ID_FIELD",
    "USER_ID_FIELD",
    "DEFAULT_EVENT_VERSION",
    "DEFAULT_EVENT_SOURCE",
    "EVENT_SEPARATOR",
    "EVENT_CREATED_SUFFIX",
    "EVENT_UPDATED_SUFFIX",
    "EVENT_DELETED_SUFFIX",
    # Exceptions
    "EventError",
    "EventRegistrationError",
    "EventAlreadyRegisteredError",
    "EventNotRegisteredError",
    "EventDispatchError",
    "EventHandlerError",
)
