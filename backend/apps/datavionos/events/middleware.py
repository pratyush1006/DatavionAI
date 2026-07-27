"""
DatavionOS Event Middleware.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable

from apps.datavionos.events.context import (
    EventContext,
)


class EventMiddleware(
    ABC,
):
    """
    Base class for all event middleware.

    Middleware executes around every
    event handler invocation.
    """

    @property
    def middleware_name(
        self,
    ) -> str:
        """
        Middleware name.
        """

        return self.__class__.__qualname__

    @property
    def priority(
        self,
    ) -> int:
        """
        Execution priority.

        Lower values execute first.
        """

        return 0

    @property
    def enabled(
        self,
    ) -> bool:
        """
        Indicates whether this
        middleware is enabled.
        """

        return True

    def before_publish(
        self,
        context: EventContext,
    ) -> None:
        """
        Invoked before a handler
        processes an event.
        """

    @abstractmethod
    def invoke(
        self,
        context: EventContext,
        next_callable: Callable[
            [],
            None,
        ],
    ) -> None:
        """
        Execute middleware logic.
        """

    def after_publish(
        self,
        context: EventContext,
    ) -> None:
        """
        Invoked after successful
        handler execution.
        """

    def on_success(
        self,
        context: EventContext,
    ) -> None:
        """
        Called after successful
        publication.
        """

    def on_failure(
        self,
        context: EventContext,
        exception: Exception,
    ) -> None:
        """
        Called when publication fails.
        """

    def __call__(
        self,
        context: EventContext,
        next_callable: Callable[
            [],
            None,
        ],
    ) -> None:
        """
        Execute middleware lifecycle.
        """

        if not self.enabled:
            next_callable()
            return

        self.before_publish(
            context,
        )

        try:
            self.invoke(
                context,
                next_callable,
            )

            self.after_publish(
                context,
            )

            self.on_success(
                context,
            )

        except Exception as exc:
            self.on_failure(
                context,
                exc,
            )
            raise

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.middleware_name}(priority={self.priority}, enabled={self.enabled})"
        )


__all__ = [
    "EventMiddleware",
]
