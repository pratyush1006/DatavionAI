"""
Duration value object.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import timedelta

from apps.domain.common import ValueObject


@dataclass(
    frozen=True,
    slots=True,
)
class Duration(
    ValueObject,
):
    """
    Immutable duration.
    """

    value: timedelta

    def _equality_components(
        self,
    ) -> tuple[object, ...]:
        return (self.value,)
