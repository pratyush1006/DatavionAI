"""
Strongly typed entity identities.
"""

from __future__ import annotations

from dataclasses import dataclass
from uuid import (
    UUID,
    uuid4,
)

from apps.domain.common.value_object import (
    ValueObject,
)


@dataclass(
    frozen=True,
    slots=True,
)
class EntityId(
    ValueObject,
):
    """
    Base entity identity.
    """

    value: UUID

    @classmethod
    def new(
        cls,
    ) -> EntityId:
        """
        Create a new identity.
        """
        return cls(
            value=uuid4(),
        )

    def _equality_components(
        self,
    ) -> tuple[object, ...]:
        return (self.value,)

    def __str__(
        self,
    ) -> str:
        return str(
            self.value,
        )
