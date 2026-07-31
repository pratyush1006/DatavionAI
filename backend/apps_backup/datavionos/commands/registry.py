"""
DatavionOS Command Handler Registry.
"""

from __future__ import annotations

from typing import Any

from apps.datavionos.commands.command import (
    Command,
)
from apps.datavionos.commands.handler import (
    CommandHandler,
)


class CommandRegistry:
    """
    Registry for command handlers.

    Maintains a one-to-one mapping between
    command types and their handlers.
    """

    def __init__(self) -> None:
        """
        Initialize registry.
        """

        self._handlers: dict[
            type[Command],
            CommandHandler[Any, Any],
        ] = {}

    @property
    def handler_count(
        self,
    ) -> int:
        """
        Number of registered handlers.
        """

        return len(
            self._handlers,
        )

    def register(
        self,
        handler: CommandHandler[Any, Any],
    ) -> None:
        """
        Register a command handler.
        """

        command_type = handler.command_type

        if command_type in self._handlers:
            raise ValueError(
                (
                    f"Handler already registered "
                    f"for command "
                    f"{command_type.__qualname__}."
                ),
            )

        self._handlers[command_type] = handler

    def unregister(
        self,
        command_type: type[Command],
    ) -> None:
        """
        Remove a handler registration.
        """

        self._handlers.pop(
            command_type,
            None,
        )

    def contains(
        self,
        command_type: type[Command],
    ) -> bool:
        """
        Determine whether a handler
        exists for a command.
        """

        return command_type in self._handlers

    def get(
        self,
        command_type: type[Command],
    ) -> CommandHandler[Any, Any]:
        """
        Retrieve a handler.
        """

        return self._handlers[command_type]

    def try_get(
        self,
        command_type: type[Command],
    ) -> CommandHandler[Any, Any] | None:
        """
        Retrieve a handler if registered.
        """

        return self._handlers.get(
            command_type,
        )

    @property
    def command_types(
        self,
    ) -> tuple[type[Command], ...]:
        """
        Registered command types.
        """

        return tuple(
            self._handlers.keys(),
        )

    @property
    def handlers(
        self,
    ) -> tuple[
        CommandHandler[Any, Any],
        ...,
    ]:
        """
        Registered handlers.
        """

        return tuple(
            self._handlers.values(),
        )

    def clear(
        self,
    ) -> None:
        """
        Remove all handler registrations.
        """

        self._handlers.clear()

    def __contains__(
        self,
        command_type: type[Command],
    ) -> bool:
        """
        Support the 'in' operator.
        """

        return self.contains(
            command_type,
        )

    def __len__(
        self,
    ) -> int:
        """
        Return the number of handlers.
        """

        return self.handler_count

    def __iter__(
        self,
    ):
        """
        Iterate over registered handlers.
        """

        return iter(
            self._handlers.values(),
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return f"{self.__class__.__name__}(handlers={self.handler_count})"


__all__ = [
    "CommandRegistry",
]
