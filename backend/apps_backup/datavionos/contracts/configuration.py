"""
Configuration contract definitions.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
)
from typing import (
    Any,
)

from apps.datavionos.contracts.base import (
    BaseContract,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class ConfigurationContract(BaseContract):
    """
    Immutable configuration definition.
    """

    identifier: str

    scope: str

    name: str

    version: str = "1.0.0"

    description: str = ""

    value: Any = None

    tenant_id: str = ""

    organization_id: str = ""

    encrypted: bool = False

    feature_flags: tuple[str, ...] = ()

    validation_rules: tuple[str, ...] = ()

    enabled: bool = True

    system: bool = False

    @property
    def qualified_name(self) -> str:
        """
        Qualified configuration name.
        """

        return f"{self.scope.value}:{self.name}:{self.version}"

    @property
    def has_feature_flags(self) -> bool:
        """
        Whether feature flags are configured.
        """

        return bool(
            self.feature_flags,
        )

    @property
    def has_validation_rules(self) -> bool:
        """
        Whether validation rules exist.
        """

        return bool(
            self.validation_rules,
        )


__all__ = [
    "ConfigurationContract",
]
