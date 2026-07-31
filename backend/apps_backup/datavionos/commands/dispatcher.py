"""
DatavionOS Command Dispatcher Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from apps.datavionos.commands.command import (
    Command,
)


class CommandDispatcher(ABC):
    """
    Base command dispatcher.

    Defines the contract for dispatching
    commands to the underlying command bus.
    """

    @property
    def dispatcher_name(self) -> str:
        """
        Dispatcher name.
        """

        return self.__class__.__name__

    @abstractmethod
    def dispatch(
        self,
        command: Command,
    ) -> Any:
        """
        Dispatch a command.

        Implementations typically delegate
        to a CommandBus.
        """

    def dispatch_many(
        self,
        *commands: Command,
    ) -> tuple[Any, ...]:
        """
        Dispatch multiple commands.
        """

        return tuple(
            self.dispatch(
                command,
            )
            for command in commands
        )

    def can_dispatch(
        self,
        command: Command,
    ) -> bool:
        """
        Determine whether the dispatcher
        can dispatch the supplied command.

        Default implementation always
        returns True.
        """

        return True

    def __call__(
        self,
        command: Command,
    ) -> Any:
        """
        Dispatch the supplied command.
        """

        return self.dispatch(
            command,
        )

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return f"{self.dispatcher_name}()"


__all__ = [
    "CommandDispatcher",
]
