"""
DatavionOS Command Exceptions.
"""

from __future__ import annotations

from apps.datavionos.commands.command import (
    Command,
)


class CommandException(Exception):
    """
    Base exception for all command
    pipeline failures.
    """

    def __init__(
        self,
        message: str,
        *,
        command_name: str = "",
    ) -> None:
        super().__init__(
            message,
        )

        self.command_name = command_name


class CommandHandlerNotFoundException(
    CommandException,
):
    """
    Raised when no handler is registered
    for a command.
    """

    def __init__(
        self,
        command_type: type[Command],
    ) -> None:
        super().__init__(
            (f"No command handler is registered for {command_type.__qualname__}."),
            command_name=command_type.__qualname__,
        )


class DuplicateCommandHandlerException(
    CommandException,
):
    """
    Raised when multiple handlers are
    registered for the same command.
    """

    def __init__(
        self,
        command_type: type[Command],
    ) -> None:
        super().__init__(
            (f"A handler has already been registered for {command_type.__qualname__}."),
            command_name=command_type.__qualname__,
        )


class CommandValidationException(
    CommandException,
):
    """
    Raised when command validation fails.
    """

    def __init__(
        self,
        message: str,
        *,
        command_name: str = "",
    ) -> None:
        super().__init__(
            message,
            command_name=command_name,
        )


class CommandAuthorizationException(
    CommandException,
):
    """
    Raised when authorization fails.
    """

    def __init__(
        self,
        message: str = ("Command authorization failed."),
        *,
        command_name: str = "",
    ) -> None:
        super().__init__(
            message,
            command_name=command_name,
        )


class CommandExecutionException(
    CommandException,
):
    """
    Raised when command execution fails.
    """

    def __init__(
        self,
        message: str,
        *,
        command_name: str = "",
        inner_exception: Exception | None = None,
    ) -> None:
        super().__init__(
            message,
            command_name=command_name,
        )

        self.inner_exception = inner_exception


class CommandTimeoutException(
    CommandException,
):
    """
    Raised when command execution
    exceeds the configured timeout.
    """

    def __init__(
        self,
        timeout_seconds: float,
        *,
        command_name: str = "",
    ) -> None:
        super().__init__(
            (f"Command execution exceeded {timeout_seconds:.2f} seconds."),
            command_name=command_name,
        )

        self.timeout_seconds = timeout_seconds


class CommandCancelledException(
    CommandException,
):
    """
    Raised when command execution
    is cancelled.
    """

    def __init__(
        self,
        *,
        command_name: str = "",
    ) -> None:
        super().__init__(
            "Command execution was cancelled.",
            command_name=command_name,
        )


class MiddlewareException(
    CommandException,
):
    """
    Raised when middleware execution
    fails.
    """

    def __init__(
        self,
        middleware_name: str,
        *,
        command_name: str = "",
        inner_exception: Exception | None = None,
    ) -> None:
        super().__init__(
            (f"Middleware {middleware_name} failed."),
            command_name=command_name,
        )

        self.middleware_name = middleware_name

        self.inner_exception = inner_exception


__all__ = [
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
