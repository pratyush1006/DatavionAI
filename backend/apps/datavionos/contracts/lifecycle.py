"""
Lifecycle contract definitions.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
)

from apps.datavionos.contracts.base import (
    BaseContract,
)
from apps.datavionos.lifecycle.state import (
    LifecycleState,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class LifecycleContract(BaseContract):
    """
    Immutable lifecycle definition.
    """

    identifier: str

    state: LifecycleState

    version: str = "1.0.0"

    description: str = ""

    tenant_id: str = ""

    organization_id: str = ""

    restartable: bool = False

    health_checkable: bool = True

    enabled: bool = True

    system: bool = False

    @property
    def qualified_name(self) -> str:
        """
        Qualified lifecycle identifier.
        """

        return f"{self.identifier}:{self.state.value}"

    @property
    def supports_restart(self) -> bool:
        """
        Whether the component supports restart.
        """

        return self.restartable

    @property
    def supports_health_check(self) -> bool:
        """
        Whether health checks are supported.
        """

        return self.health_checkable


__all__ = [
    "LifecycleContract",
]
