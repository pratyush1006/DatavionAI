"""
Scheduler service aggregation.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.datavionos.scheduler.dispatcher import (
    SchedulerDispatcher,
)
from apps.datavionos.scheduler.engine import (
    SchedulerEngine,
)
from apps.datavionos.scheduler.registry import (
    SchedulerRegistry,
)
from apps.datavionos.scheduler.trigger import (
    TriggerEvaluator,
)


@dataclass(
    frozen=True,
    slots=True,
)
class SchedulerServices:
    """
    Aggregate of scheduler services.
    """

    engine: SchedulerEngine

    registry: SchedulerRegistry

    dispatcher: SchedulerDispatcher

    trigger_evaluator: TriggerEvaluator


__all__ = [
    "SchedulerServices",
]
