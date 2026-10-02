"""
Event type definitions for DatavionOS.

Provides reusable type aliases and protocols used by the
platform event framework.

Business applications should define their own event payloads
and event names while using these shared contracts.
"""

from __future__ import annotations

from collections.abc import (
    Callable,
    Mapping,
)
from typing import (
    Any,
    Protocol,
)

###############################################################################
# Event Names
###############################################################################

type EventName = str


###############################################################################
# Event Identifiers
###############################################################################

type EventID = str


###############################################################################
# Event Payloads
###############################################################################

type EventPayload = Mapping[
    str,
    Any,
]


###############################################################################
# Event Metadata
###############################################################################

type EventMetadata = Mapping[
    str,
    Any,
]


###############################################################################
# Event Handler
###############################################################################


class EventHandler(
    Protocol,
):
    """
    Protocol for event handlers.

    Event handlers consume dispatched events and execute
    application-specific actions.
    """

    def __call__(
        self,
        event: Any,
    ) -> Any:
        """
        Handle an event.
        """


###############################################################################
# Event Callback
###############################################################################

type EventCallback = Callable[
    [Any],
    Any,
]


__all__: tuple[str, ...] = (
    "EventCallback",
    "EventHandler",
    "EventID",
    "EventMetadata",
    "EventName",
    "EventPayload",
)
