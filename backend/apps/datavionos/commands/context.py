"""
DatavionOS Command Execution Context.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4

from apps.datavionos.commands.command import (
    Command,
)
from apps.datavionos.container.container import (
    Container,
)


@dataclass(
    slots=True,
    kw_only=True,
)
class CommandContext:
    """
    Runtime context shared throughout
    command execution.
    """

    command: Command

    services: Container

    correlation_id: str = ""

    causation_id: str = ""

    request_id: str = field(
        default_factory=lambda: str(
            uuid4(),
        ),
    )

    tenant_id: str = ""

    organization_id: str = ""

    user_id: str = ""

    started_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    items: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def command_name(self) -> str:
        """
        Command name.
        """

        return self.command.command_name

    @property
    def has_user(self) -> bool:
        """
        Whether a user is present.
        """

        return bool(
            self.user_id,
        )

    @property
    def has_tenant(self) -> bool:
        """
        Whether a tenant is present.
        """

        return bool(
            self.tenant_id,
        )

    @property
    def has_organization(self) -> bool:
        """
        Whether an organization is present.
        """

        return bool(
            self.organization_id,
        )

    @property
    def has_correlation(self) -> bool:
        """
        Whether a correlation identifier
        exists.
        """

        return bool(
            self.correlation_id,
        )

    @property
    def metadata_count(self) -> int:
        """
        Number of metadata entries.
        """

        return len(
            self.metadata,
        )

    def set_item(
        self,
        key: str,
        value: Any,
    ) -> None:
        """
        Store a runtime item.
        """

        self.items[key] = value

    def get_item(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        """
        Retrieve a runtime item.
        """

        return self.items.get(
            key,
            default,
        )

    def contains_item(
        self,
        key: str,
    ) -> bool:
        """
        Determine whether a runtime item
        exists.
        """

        return key in self.items

    def remove_item(
        self,
        key: str,
    ) -> None:
        """
        Remove a runtime item.
        """

        self.items.pop(
            key,
            None,
        )

    def clear_items(
        self,
    ) -> None:
        """
        Clear all runtime items.
        """

        self.items.clear()

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"command={self.command_name!r}, "
            f"tenant={self.tenant_id!r}, "
            f"user={self.user_id!r})"
        )


__all__ = [
    "CommandContext",
]
