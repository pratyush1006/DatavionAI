"""
DatavionOS Command Handler Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TypeVar

from apps.datavionos.commands.command import (
    Command,
)

TCommand = TypeVar(
    "TCommand",
    bound=Command,
)

TResult = TypeVar(
    "TResult",
)


class CommandHandler[TCommand, TResult](ABC):
    """
    Base command handler.

    A command handler is responsible for
    executing exactly one command type.
    """

    @property
    def command_type(
        self,
    ) -> type[TCommand]:
        """
        Command handled by this handler.
        """

        return self.__orig_bases__[0].__args__[0]

    @property
    def handler_name(
        self,
    ) -> str:
        """
        Handler name.
        """

        return self.__class__.__name__

    def can_handle(
        self,
        command: Command,
    ) -> bool:
        """
        Determine whether this handler can
        execute the supplied command.
        """

        return isinstance(
            command,
            self.command_type,
        )

    @abstractmethod
    def handle(
        self,
        command: TCommand,
    ) -> TResult:
        """
        Execute the command.

        Must be implemented by subclasses.
        """

    def __call__(
        self,
        command: TCommand,
    ) -> TResult:
        """
        Execute the handler.
        """

        return self.handle(
            command,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return f"{self.handler_name}(command={self.command_type.__name__})"


__all__ = [
    "CommandHandler",
]
