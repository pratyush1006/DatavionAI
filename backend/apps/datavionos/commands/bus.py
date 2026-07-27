"""
DatavionOS Command Bus.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from apps.datavionos.commands.command import (
    Command,
)
from apps.datavionos.commands.dispatcher import (
    CommandDispatcher,
)
from apps.datavionos.commands.handler import (
    CommandHandler,
)
from apps.datavionos.commands.middleware import (
    CommandMiddleware,
)
from apps.datavionos.commands.registry import (
    CommandRegistry,
)


class CommandBus(CommandDispatcher):
    """
    Default in-process command bus.

    Responsible for locating the
    appropriate handler and executing
    the middleware pipeline.
    """

    def __init__(
        self,
        registry: CommandRegistry,
    ) -> None:
        """
        Initialize command bus.
        """

        self._registry = registry

        self._middleware: list[Any] = []

    @property
    def registry(
        self,
    ) -> CommandRegistry:
        """
        Command registry.
        """

        return self._registry

    @property
    def middleware_count(
        self,
    ) -> int:
        """
        Number of registered middleware.
        """

        return len(
            self._middleware,
        )

    def register(
        self,
        handler: CommandHandler[Any, Any],
    ) -> None:
        """
        Register a command handler.
        """

        self._registry.register(
            handler,
        )

    def add_middleware(
        self,
        middleware: CommandMiddleware,
    ) -> None:
        """
        Register command middleware.
        """

        self._middleware.append(
            middleware,
        )

    def remove_middleware(
        self,
        middleware: Any,
    ) -> None:
        """
        Remove middleware if registered.
        """

        if middleware in self._middleware:
            self._middleware.remove(
                middleware,
            )

    def clear_middleware(
        self,
    ) -> None:
        """
        Remove all registered middleware.
        """

        self._middleware.clear()

    def has_middleware(
        self,
        middleware: Any,
    ) -> bool:
        """
        Determine whether middleware is registered.
        """

        return middleware in self._middleware

    def _build_pipeline(
        self,
        command: Command,
        handler: CommandHandler[Any, Any],
    ) -> Any:
        """
        Build the middleware execution pipeline.
        """

        def terminal() -> Any:
            return handler.handle(
                command,
            )

        next_callable = terminal

        for middleware in reversed(
            self._middleware,
        ):
            current = middleware

            def make_next(
                inner: CommandMiddleware,
                outer: Callable[[], Any],
            ) -> Callable[[], Any]:
                def step() -> Any:
                    return inner(
                        command,
                        outer,
                    )

                return step

            next_callable = make_next(
                current,
                next_callable,
            )

        return next_callable()

    def dispatch(
        self,
        command: Command,
    ) -> Any:
        """
        Dispatch a command through the pipeline.
        """

        handler = self._registry.get(
            type(command),
        )

        return self._build_pipeline(
            command,
            handler,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.__class__.__name__}("
            f"handlers={self.registry.handler_count}, "
            f"middleware={self.middleware_count})"
        )


__all__ = [
    "CommandBus",
]
