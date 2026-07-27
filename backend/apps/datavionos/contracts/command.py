"""
Command contract definitions.
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
class CommandContract(BaseContract):
    """
    Immutable command definition.
    """

    identifier: str

    command_type: str

    version: str = "1.0.0"

    description: str = ""

    tenant_id: str = ""

    organization_id: str = ""

    retryable: bool = False

    idempotent: bool = False

    requires_auth: bool = True

    enabled: bool = True

    system: bool = False

    @property
    def qualified_name(self) -> str:
        """
        Qualified command name.
        """

        return f"{self.command_type}:{self.version}"

    @property
    def belongs_to_tenant(self) -> bool:
        """
        Whether the command belongs to a tenant.
        """

        return bool(
            self.tenant_id,
        )

    @property
    def supports_retry(self) -> bool:
        """
        Whether the command supports retries.
        """

        return self.retryable


__all__ = [
    "CommandContract",
]
