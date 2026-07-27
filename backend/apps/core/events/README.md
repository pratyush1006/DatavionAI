# DatavionAI Core Event Framework

The DatavionAI event framework provides a lightweight publish/subscribe
mechanism for domain events.

## Components

- DomainEvent
- EventRegistry
- EventDispatcher
- EventPublisher
- EventHandler

## Example

```python
from dataclasses import dataclass
from uuid import UUID

from apps.core.events import (
    DomainEvent,
    EventHandler,
    publisher,
    registry,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OrganizationCreatedEvent(
    DomainEvent,
):
    organization_id: UUID


class AuditHandler:
    def handle(
        self,
        event: DomainEvent,
    ) -> None:
        print(event)


registry.register(
    OrganizationCreatedEvent,
    AuditHandler(),
)

publisher.publish(
    OrganizationCreatedEvent(
        organization_id=UUID("00000000-0000-0000-0000-000000000001"),
    ),
)
```

## Design Goals

- Immutable domain events
- Loose coupling
- Strong typing
- Simple synchronous dispatch
- Extensible for asynchronous messaging
