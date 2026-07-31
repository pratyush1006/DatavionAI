"""
DatavionOS Command Processing Framework.

This package provides the foundational CQRS command
infrastructure used throughout DatavionOS.

Public API:
    - Command
    - CommandHandler
    - CommandDispatcher
    - CommandRegistry
    - CommandBus
    - CommandMiddleware
    - CommandContext
    - CommandResult

Exceptions:
    - CommandException
    - CommandHandlerNotFoundException
    - DuplicateCommandHandlerException
    - CommandValidationException
    - CommandAuthorizationException
    - CommandExecutionException
    - CommandTimeoutException
    - CommandCancelledException
    - MiddlewareException
"""

from __future__ import annotations

from apps.datavionos.commands.bus import (
    CommandBus,
)
from apps.datavionos.commands.command import (
    Command,
)
from apps.datavionos.commands.context import (
    CommandContext,
)
from apps.datavionos.commands.dispatcher import (
    CommandDispatcher,
)
from apps.datavionos.commands.exceptions import (
    CommandAuthorizationException,
    CommandCancelledException,
    CommandException,
    CommandExecutionException,
    CommandHandlerNotFoundException,
    CommandTimeoutException,
    CommandValidationException,
    DuplicateCommandHandlerException,
    MiddlewareException,
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
from apps.datavionos.commands.result import (
    CommandResult,
)

__all__ = [
    # Core Contracts
    "Command",
    "CommandHandler",
    "CommandDispatcher",
    "CommandRegistry",
    "CommandBus",
    "CommandMiddleware",
    "CommandContext",
    "CommandResult",
    # Exceptions
    "CommandException",
    "CommandHandlerNotFoundException",
    "DuplicateCommandHandlerException",
    "CommandValidationException",
    "CommandAuthorizationException",
    "CommandExecutionException",
    "CommandTimeoutException",
    "CommandCancelledException",
    "MiddlewareException",
]
