"""
Organization name value object.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.domain.common import ValueObject
from apps.domain.common.exceptions import (
    InvalidValueObjectException,
)


@dataclass(
    frozen=True,
    slots=True,
)
class OrganizationName(
    ValueObject,
):
    """
    Organization name.
    """

    value: str

    MIN_LENGTH: int = 2
    MAX_LENGTH: int = 150

    def __post_init__(
        self,
    ) -> None:
        normalized = " ".join(
            self.value.strip().split(),
        )

        if not normalized:
            raise InvalidValueObjectException(
                "Organization name cannot be empty.",
            )

        if len(normalized) < self.MIN_LENGTH:
            raise InvalidValueObjectException(
                f"Organization name must contain at least {self.MIN_LENGTH} characters.",
            )

        if len(normalized) > self.MAX_LENGTH:
            raise InvalidValueObjectException(
                f"Organization name cannot exceed {self.MAX_LENGTH} characters.",
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )

    def _equality_components(
        self,
    ) -> tuple[object, ...]:
        return (self.value.casefold(),)

    def __str__(
        self,
    ) -> str:
        return self.value
