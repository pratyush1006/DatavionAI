"""
Distributed cache lock.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from contextlib import AbstractContextManager


class CacheLock(
    AbstractContextManager["CacheLock"],
    ABC,
):
    """
    Abstract distributed cache lock.

    Concrete implementations are responsible for providing
    backend-specific locking (Redis, Memcached, etc.).
    """

    @property
    @abstractmethod
    def name(
        self,
    ) -> str:
        """
        Return the lock name.
        """

    @property
    @abstractmethod
    def locked(
        self,
    ) -> bool:
        """
        Return whether the lock is currently held.
        """

    @abstractmethod
    def acquire(
        self,
        *,
        blocking: bool = True,
        timeout: float | None = None,
    ) -> bool:
        """
        Acquire the lock.

        Returns:
            True if the lock was acquired.
        """

    @abstractmethod
    def release(
        self,
    ) -> None:
        """
        Release the lock.
        """

    def __enter__(
        self,
    ) -> CacheLock:
        """
        Enter the runtime context.
        """

        if not self.acquire():
            raise RuntimeError(
                "Unable to acquire cache lock.",
            )

        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: object | None,
    ) -> None:
        """
        Exit the runtime context.
        """

        if self.locked:
            self.release()


__all__: tuple[str, ...] = ("CacheLock",)
