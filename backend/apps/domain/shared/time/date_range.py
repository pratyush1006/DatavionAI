"""
Date range value object.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from apps.domain.common import ValueObject


@dataclass(
    frozen=True,
    slots=True,
)
class DateRange(
    ValueObject,
):
    """
    Immutable date range.
    """

    start: datetime

    end: datetime

    def _equality_components(
        self,
    ) -> tuple[object, ...]:
        return (
            self.start,
            self.end,
        )

    def contains(
        self,
        value: datetime,
    ) -> bool:
        return self.start <= value <= self.end

    def overlaps(
        self,
        other: DateRange,
    ) -> bool:
        return self.start <= other.end and other.start <= self.end
