"""
DatavionOS Command Middleware Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Callable
from typing import Any

from apps.datavionos.commands.command import (
    Command,
)


class CommandMiddleware(ABC):
    """
    Base middleware for the command pipeline.

    Middleware participates in command
    execution before and after the handler
    executes.
    """

    @property
    def middleware_name(self) -> str:
        """
        Middleware name.
        """

        return self.__class__.__name__

    @property
    def priority(self) -> int:
        """
        Execution priority.

        Lower values execute earlier.
        """

        return 0

    def before_dispatch(
        self,
        command: Command,
    ) -> None:
        """
        Executed before the command enters
        the pipeline.
        """

    @abstractmethod
    def invoke(
        self,
        command: Command,
        next_callable: Callable[[], Any],
    ) -> Any:
        """
        Execute middleware.

        Must call next_callable() to
        continue pipeline execution.
        """

    def after_dispatch(
        self,
        command: Command,
        result: Any,
    ) -> Any:
        """
        Executed after successful
        command execution.
        """

        return result

    def on_success(
        self,
        command: Command,
        result: Any,
    ) -> None:
        """
        Called after successful
        execution.
        """

    def on_failure(
        self,
        command: Command,
        exception: Exception,
    ) -> None:
        """
        Called when execution fails.
        """

    def __call__(
        self,
        command: Command,
        next_callable: Callable[[], Any],
    ) -> Any:
        """
        Execute middleware lifecycle.
        """

        self.before_dispatch(
            command,
        )

        try:
            result = self.invoke(
                command,
                next_callable,
            )

            result = self.after_dispatch(
                command,
                result,
            )

            self.on_success(
                command,
                result,
            )

            return result

        except Exception as exc:
            self.on_failure(
                command,
                exc,
            )
            raise

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return f"{self.middleware_name}(priority={self.priority})"


__all__ = [
    "CommandMiddleware",
]
