"""
Workflow contract definitions.
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
class WorkflowContract(BaseContract):
    """
    Immutable workflow definition.
    """

    identifier: str

    version: str = "1.0.0"

    description: str = ""

    tenant_id: str = ""

    organization_id: str = ""

    retryable: bool = False

    system: bool = False

    enabled: bool = True

    @property
    def qualified_name(self) -> str:
        """
        Qualified workflow name.
        """

        return f"{self.identifier}:{self.version}"

    @property
    def supports_retry(self) -> bool:
        """
        Whether the workflow supports retries.
        """

        return self.retryable

    @property
    def is_system_workflow(self) -> bool:
        """
        Whether the workflow is system managed.
        """

        return self.system


__all__ = [
    "WorkflowContract",
]
