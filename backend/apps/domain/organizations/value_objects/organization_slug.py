"""
Organization slug value object.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from apps.domain.common import ValueObject
from apps.domain.common.exceptions import (
    InvalidValueObjectException,
)

_SLUG_PATTERN = re.compile(
    r"^[a-z0-9]+(?:-[a-z0-9]+)*$",
)


@dataclass(
    frozen=True,
    slots=True,
)
class OrganizationSlug(
    ValueObject,
):
    """
    Organization slug.
    """

    value: str

    MIN_LENGTH: int = 3
    MAX_LENGTH: int = 100

    def __post_init__(
        self,
    ) -> None:
        normalized = self.value.strip().lower()

        if not normalized:
            raise InvalidValueObjectException(
                "Organization slug cannot be empty.",
            )

        if len(normalized) < self.MIN_LENGTH:
            raise InvalidValueObjectException(
                f"Organization slug must contain at least {self.MIN_LENGTH} characters.",
            )

        if len(normalized) > self.MAX_LENGTH:
            raise InvalidValueObjectException(
                f"Organization slug cannot exceed {self.MAX_LENGTH} characters.",
            )

        if not _SLUG_PATTERN.fullmatch(normalized):
            raise InvalidValueObjectException(
                "Organization slug must contain only lowercase letters, numbers, and hyphens.",
            )

        object.__setattr__(
            self,
            "value",
            normalized,
        )

    def _equality_components(
        self,
    ) -> tuple[object, ...]:
        return (self.value,)

    def __str__(
        self,
    ) -> str:
        return self.value
