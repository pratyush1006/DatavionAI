"""
Event handler contracts for DatavionOS.

Defines reusable handler abstractions used by the event framework.

Handlers are responsible for reacting to dispatched events.

Business applications implement concrete handlers inside their
own modules.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import Any

from apps.common.events.models import (
    Event,
)


class BaseEventHandler(
    ABC,
):
    """
    Base class for all DatavionOS event handlers.

    Application-specific handlers should inherit from this class.

    Example:

        class PatientRegisteredHandler(BaseEventHandler):
            event_name = "patient.registered"
    """

    event_name: str = ""

    @abstractmethod
    def handle(
        self,
        event: Event,
    ) -> Any:
        """
        Process an event.

        Implementations should contain business logic.
        """


class FunctionEventHandler:
    """
    Adapter for function-based event handlers.

    Allows simple functions to participate in the event system.
    """

    def __init__(
        self,
        callback: Any,
    ) -> None:
        """
        Initialize handler adapter.
        """

        self.callback = callback

    def handle(
        self,
        event: Event,
    ) -> Any:
        """
        Execute wrapped callback.
        """

        return self.callback(
            event,
        )


__all__: tuple[str, ...] = (
    "BaseEventHandler",
    "FunctionEventHandler",
)
