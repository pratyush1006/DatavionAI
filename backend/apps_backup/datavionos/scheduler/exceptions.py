"""
Scheduler exceptions.
"""

from __future__ import annotations


class SchedulerError(Exception):
    """
    Base scheduler exception.
    """


class ScheduleError(SchedulerError):
    """
    Raised when a schedule operation fails.
    """


class TriggerError(SchedulerError):
    """
    Raised when trigger evaluation fails.
    """


class JobExecutionError(SchedulerError):
    """
    Raised when job execution fails.
    """


class DispatcherError(SchedulerError):
    """
    Raised when dispatching a job fails.
    """


class RegistryError(SchedulerError):
    """
    Raised when registry operations fail.
    """


class EngineError(SchedulerError):
    """
    Raised when the scheduler engine fails.
    """


__all__ = [
    "SchedulerError",
    "ScheduleError",
    "TriggerError",
    "JobExecutionError",
    "DispatcherError",
    "RegistryError",
    "EngineError",
]
