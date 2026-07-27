"""
DatavionOS Query Contract.
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any
from uuid import uuid4


@dataclass(
    slots=True,
    frozen=True,
    kw_only=True,
)
class Query(ABC):
    """
    Base class for all CQRS queries.

    Queries represent immutable requests
    for information and must not modify
    application state.
    """

    query_id: str = field(
        default_factory=lambda: str(
            uuid4(),
        ),
    )

    created_at: datetime = field(
        default_factory=lambda: datetime.now(
            UTC,
        ),
    )

    metadata: dict[str, Any] = field(
        default_factory=dict,
    )

    @property
    def query_name(
        self,
    ) -> str:
        """
        Fully qualified query name.
        """

        return self.__class__.__qualname__

    def with_metadata(
        self,
        **metadata: Any,
    ) -> Query:
        """
        Return a copy of the query with
        additional metadata.
        """

        merged = {
            **self.metadata,
            **metadata,
        }

        return self.__class__(
            query_id=self.query_id,
            created_at=self.created_at,
            metadata=merged,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return f"{self.query_name}(id={self.query_id!r})"


__all__ = [
    "Query",
]
