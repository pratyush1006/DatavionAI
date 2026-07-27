"""Base contract definitions for the DatavionOS kernel.

Contracts are immutable value objects that define the public interfaces
shared between the DatavionOS kernel, platform services, plugins, and
applications.

All DatavionOS contracts should inherit from ``BaseContract`` to ensure
consistent serialization, validation, equality semantics, and debugging
behaviour across the platform.
"""

from __future__ import annotations

from dataclasses import (
    asdict,
    dataclass,
)
from typing import (
    Any,
    Final,
)


@dataclass(
    frozen=True,
    kw_only=True,
    slots=True,
)
class BaseContract:
    """Immutable base class for all DatavionOS contracts.

    All contracts expose a stable keyword-only identity via ``identifier``.
    """

    identifier: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize the contract into a dictionary."""
        return asdict(self)

    @classmethod
    def contract_name(cls) -> str:
        """Return the contract class name."""
        return cls.__name__

    @classmethod
    def contract_namespace(cls) -> str:
        """Return the fully qualified contract namespace."""
        return f"{cls.__module__}.{cls.__qualname__}"

    @classmethod
    def contract_version(cls) -> int:
        """Return the contract schema version."""
        return 1

    @property
    def schema(self) -> str:
        """Return the schema identifier."""
        return f"{self.contract_namespace()}:v{self.contract_version()}"


CONTRACT_SCHEMA_VERSION: Final[int] = 1

__all__ = [
    "BaseContract",
    "CONTRACT_SCHEMA_VERSION",
]
