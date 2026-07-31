"""
Command messaging contracts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import (
    Protocol,
    runtime_checkable,
)

from apps.datavionos.messaging.message import (
    Message,
)


@dataclass(
    frozen=True,
    slots=True,
)
class Command(
    Message,
):
    """
    Base command contract.

    A command represents an instruction to perform
    a single action.
    """


@runtime_checkable
class CommandHandler(
    Protocol,
):
    """
    Handles a command.
    """

    async def handle(
        self,
        command: Command,
    ) -> None:
        """
        Handle a command.
        """


@runtime_checkable
class CommandDispatcher(
    Protocol,
):
    """
    Dispatches commands to their handler.
    """

    async def dispatch(
        self,
        command: Command,
    ) -> None:
        """
        Dispatch a command.
        """


__all__ = [
    "Command",
    "CommandDispatcher",
    "CommandHandler",
]
