"""
Metadata contract definitions for the DatavionOS kernel.

Metadata accompanies contracts throughout the DatavionOS runtime to provide
consistent identity, versioning, provenance, and traceability.

The metadata contract is intentionally immutable and framework agnostic so it
can safely be used by plugins, events, workflows, integrations, APIs, and
background jobs.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Final
from uuid import uuid4

from apps.datavionos.contracts.base import BaseContract

DEFAULT_SCHEMA_VERSION: Final[int] = 1


@dataclass(
    frozen=True,
    kw_only=True,
    slots=True,
)
class ContractMetadata(BaseContract):
    """
    Metadata describing a DatavionOS contract.

    Attributes:
        identifier:
            Globally unique identifier for the contract instance.

        contract:
            Human-readable contract name.

        version:
            Contract schema version.

        namespace:
            Fully-qualified contract namespace.

        created_at:
            UTC timestamp when the metadata instance was created.

        source:
            Optional producer of the contract
            (plugin, service, integration, etc.).
    """

    identifier: str

    contract: str

    version: int = DEFAULT_SCHEMA_VERSION

    namespace: str = ""

    created_at: datetime = datetime.now(UTC)

    source: str | None = None

    @classmethod
    def create(
        cls,
        *,
        contract: type[BaseContract],
        source: str | None = None,
    ) -> ContractMetadata:
        """
        Create metadata for a contract class.

        Args:
            contract:
                Contract type.

            source:
                Optional producer identifier.

        Returns:
            A populated metadata instance.
        """
        return cls(
            identifier=str(uuid4()),
            contract=contract.contract_name(),
            version=contract.contract_version(),
            namespace=contract.contract_namespace(),
            created_at=datetime.now(UTC),
            source=source,
        )

    @property
    def schema(self) -> str:
        """
        Return the metadata schema identifier.

        Example:
            apps.datavionos.contracts.PluginContract:v1
        """
        return f"{self.namespace}:v{self.version}"

    @property
    def is_version_supported(self) -> bool:
        """
        Determine whether this metadata references a supported schema.

        Returns:
            True when the schema version is supported.
        """
        return self.version >= DEFAULT_SCHEMA_VERSION


__all__ = [
    "ContractMetadata",
    "DEFAULT_SCHEMA_VERSION",
]
