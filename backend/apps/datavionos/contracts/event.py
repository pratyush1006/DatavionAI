"""
Event contract definitions.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
)

from apps.datavionos.contracts.base import (
    BaseContract,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class EventContract(BaseContract):
    """
    Immutable event definition.
    """

    identifier: str

    event_type: str

    version: str = "1.0.0"

    description: str = ""

    tenant_id: str = ""

    organization_id: str = ""

    replayable: bool = False

    durable: bool = False

    encrypted: bool = False

    enabled: bool = True

    system: bool = False

    @property
    def qualified_name(self) -> str:
        """
        Qualified event name.
        """

        return f"{self.event_type}:{self.version}"

    @property
    def supports_replay(self) -> bool:
        """
        Whether the event supports replay.
        """

        return self.replayable

    @property
    def is_durable(self) -> bool:
        """
        Whether the event is durable.
        """

        return self.durable


__all__ = [
    "EventContract",
]
