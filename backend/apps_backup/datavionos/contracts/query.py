"""
Query contract definitions.
"""

from __future__ import annotations

from dataclasses import (
    dataclass,
    replace,
)

from apps.datavionos.contracts.base import (
    BaseContract,
)


@dataclass(
    frozen=True,
    slots=True,
    kw_only=True,
)
class QueryContract(BaseContract):
    """
    Immutable query definition.
    """

    identifier: str

    query_type: str

    version: str = "1.0.0"

    description: str = ""

    status: str = "pending"

    tenant_id: str = ""

    organization_id: str = ""

    retryable: bool = False

    cacheable: bool = False

    enabled: bool = True

    system: bool = False

    @property
    def qualified_name(self) -> str:
        """
        Qualified query name.
        """

        return f"{self.query_type}:{self.version}"

    def with_status(
        self,
        status: str,
    ) -> QueryContract:
        """
        Return a copy with a new query status.
        """

        return replace(
            self,
            status=status,
        )

    @property
    def supports_retry(self) -> bool:
        """
        Whether the query supports retries.
        """

        return self.retryable


__all__ = [
    "QueryContract",
]
