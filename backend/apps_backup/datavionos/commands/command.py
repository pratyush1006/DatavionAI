"""
DatavionOS Command Contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class Command:
    """
    Base command.

    Represents an immutable intent to
    change the state of the system.
    """

    command_id: str = field(
        default_factory=lambda: str(
            uuid4(),
        ),
    )

    correlation_id: str = ""

    causation_id: str = ""

    tenant_id: str = ""

    organization_id: str = ""

    user_id: str = ""

    requested_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def command_name(self) -> str:
        """
        Name of the command.
        """

        return self.__class__.__name__

    @property
    def has_correlation(self) -> bool:
        """
        Whether a correlation identifier
        is present.
        """

        return bool(
            self.correlation_id,
        )

    @property
    def has_causation(self) -> bool:
        """
        Whether a causation identifier
        is present.
        """

        return bool(
            self.causation_id,
        )

    @property
    def belongs_to_tenant(self) -> bool:
        """
        Whether the command belongs to
        a tenant.
        """

        return bool(
            self.tenant_id,
        )

    @property
    def belongs_to_organization(
        self,
    ) -> bool:
        """
        Whether the command belongs to
        an organization.
        """

        return bool(
            self.organization_id,
        )

    @property
    def has_user(self) -> bool:
        """
        Whether the command has an
        associated user.
        """

        return bool(
            self.user_id,
        )

    @property
    def metadata_count(self) -> int:
        """
        Number of metadata entries.
        """

        return len(
            self.metadata,
        )

    def with_metadata(
        self,
        **metadata: Any,
    ) -> Command:
        """
        Return a copy with merged
        metadata.
        """

        from dataclasses import replace

        return replace(
            self,
            metadata={
                **self.metadata,
                **metadata,
            },
        )

    def to_dict(
        self,
    ) -> dict[str, Any]:
        """
        Serialize the command.
        """

        return {
            "command_id": self.command_id,
            "command_name": self.command_name,
            "correlation_id": self.correlation_id,
            "causation_id": self.causation_id,
            "tenant_id": self.tenant_id,
            "organization_id": (self.organization_id),
            "user_id": self.user_id,
            "requested_at": (self.requested_at.isoformat()),
            "metadata": dict(
                self.metadata,
            ),
        }

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return f"{self.command_name}(id={self.command_id!r}, tenant={self.tenant_id!r})"


__all__ = [
    "Command",
]
