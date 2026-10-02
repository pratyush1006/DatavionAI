"""
DatavionOS lifecycle events.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import (
    Any,
)

from apps.datavionos.lifecycle.state import (
    LifecycleState,
)


@dataclass(
    frozen=True,
    slots=True,
)
class LifecycleEvent:
    """
    Base lifecycle event.
    """

    event_name: str

    component_id: str

    component_name: str

    state: LifecycleState

    occurred_at: datetime

    correlation_id: str = ""

    tenant_id: str = ""

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def has_metadata(self) -> bool:
        """
        Whether metadata exists.
        """

        return bool(
            self.metadata,
        )

    @property
    def metadata_count(self) -> int:
        """
        Number of metadata entries.
        """

        return len(
            self.metadata,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the lifecycle event.
        """

        return {
            "event_name": self.event_name,
            "component_id": self.component_id,
            "component_name": self.component_name,
            "state": self.state.value,
            "occurred_at": self.occurred_at.isoformat(),
            "correlation_id": self.correlation_id,
            "tenant_id": self.tenant_id,
            "metadata": dict(
                self.metadata,
            ),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> LifecycleEvent:
        """
        Create a lifecycle event from a dictionary.
        """

        return cls(
            event_name=data["event_name"],
            component_id=data["component_id"],
            component_name=data["component_name"],
            state=LifecycleState(
                data["state"],
            ),
            occurred_at=datetime.fromisoformat(
                data["occurred_at"],
            ),
            correlation_id=data.get(
                "correlation_id",
                "",
            ),
            tenant_id=data.get(
                "tenant_id",
                "",
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )

    def __repr__(self) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.event_name}("
            f"component_id={self.component_id!r}, "
            f"state={self.state.value!r})"
        )


@dataclass(
    frozen=True,
    slots=True,
)
class InitializedEvent(LifecycleEvent):
    """
    Component initialized.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class StartedEvent(LifecycleEvent):
    """
    Component started.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class PausedEvent(LifecycleEvent):
    """
    Component paused.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class ResumedEvent(LifecycleEvent):
    """
    Component resumed.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class StoppedEvent(LifecycleEvent):
    """
    Component stopped.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class RestartedEvent(LifecycleEvent):
    """
    Component restarted.
    """


@dataclass(
    frozen=True,
    slots=True,
)
class FailedEvent(LifecycleEvent):
    """
    Component failed.
    """

    exception: str = ""


@dataclass(
    frozen=True,
    slots=True,
)
class TerminatedEvent(LifecycleEvent):
    """
    Component terminated.
    """

    @property
    def metadata_count(self) -> int:
        """
        Number of metadata entries.
        """

        return len(
            self.metadata,
        )

    def to_dict(self) -> dict[str, Any]:
        """
        Serialize the lifecycle event.
        """

        return {
            "event_name": self.event_name,
            "component_id": self.component_id,
            "component_name": self.component_name,
            "state": self.state.value,
            "occurred_at": self.occurred_at.isoformat(),
            "correlation_id": self.correlation_id,
            "tenant_id": self.tenant_id,
            "metadata": dict(
                self.metadata,
            ),
        }

    @classmethod
    def from_dict(
        cls,
        data: dict[str, Any],
    ) -> LifecycleEvent:
        """
        Create a lifecycle event from
        a dictionary.
        """

        return cls(
            event_name=data["event_name"],
            component_id=data["component_id"],
            component_name=data["component_name"],
            state=LifecycleState(
                data["state"],
            ),
            occurred_at=datetime.fromisoformat(
                data["occurred_at"],
            ),
            correlation_id=data.get(
                "correlation_id",
                "",
            ),
            tenant_id=data.get(
                "tenant_id",
                "",
            ),
            metadata=data.get(
                "metadata",
                {},
            ),
        )

    def __repr__(self) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.event_name}("
            f"component_id={self.component_id!r}, "
            f"state={self.state.value!r})"
        )


EVENT_TYPES: dict[
    str,
    type[LifecycleEvent],
] = {
    "initialized": InitializedEvent,
    "started": StartedEvent,
    "paused": PausedEvent,
    "resumed": ResumedEvent,
    "stopped": StoppedEvent,
    "restarted": RestartedEvent,
    "failed": FailedEvent,
    "terminated": TerminatedEvent,
}


__all__ = [
    "LifecycleEvent",
    "InitializedEvent",
    "StartedEvent",
    "PausedEvent",
    "ResumedEvent",
    "StoppedEvent",
    "RestartedEvent",
    "FailedEvent",
    "TerminatedEvent",
    "EVENT_TYPES",
]
