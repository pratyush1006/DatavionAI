"""
Scheduler trigger contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import (
    datetime,
)
from enum import StrEnum
from typing import (
    Any,
    Protocol,
    runtime_checkable,
)


class TriggerType(
    StrEnum,
):
    """
    Supported trigger types.
    """

    ONCE = "once"

    INTERVAL = "interval"

    CRON = "cron"

    EVENT = "event"

    MANUAL = "manual"


@dataclass(
    frozen=True,
    slots=True,
)
class Trigger:
    """
    Immutable scheduler trigger.
    """

    id: str

    type: TriggerType

    next_run: datetime

    expression: str | None = None

    metadata: dict[str, Any] | None = None


@runtime_checkable
class TriggerEvaluator(
    Protocol,
):
    """
    Evaluates scheduler triggers.
    """

    async def should_fire(
        self,
        trigger: Trigger,
        now: datetime | None = None,
    ) -> bool:
        """
        Determine whether the trigger
        should execute.
        """

    async def next_execution(
        self,
        trigger: Trigger,
        after: datetime | None = None,
    ) -> datetime | None:
        """
        Return the next execution time.
        """


__all__ = [
    "Trigger",
    "TriggerEvaluator",
    "TriggerType",
]
