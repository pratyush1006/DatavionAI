"""
DatavionOS Service Contracts.
"""

from __future__ import annotations

from abc import ABC, abstractmethod


class Service(
    ABC,
):
    """
    Base contract for every service
    managed by the DatavionOS
    dependency injection container.
    """


class Disposable(
    ABC,
):
    """
    Represents a synchronously
    disposable service.
    """

    @abstractmethod
    def dispose(
        self,
    ) -> None:
        """
        Release owned resources.
        """


class AsyncDisposable(
    ABC,
):
    """
    Represents an asynchronously
    disposable service.
    """

    @abstractmethod
    async def dispose_async(
        self,
    ) -> None:
        """
        Release owned resources
        asynchronously.
        """


class Initializable(
    ABC,
):
    """
    Represents a service requiring
    initialization after creation.
    """

    @abstractmethod
    def initialize(
        self,
    ) -> None:
        """
        Initialize the service.
        """


class AsyncInitializable(
    ABC,
):
    """
    Represents a service requiring
    asynchronous initialization.
    """

    @abstractmethod
    async def initialize_async(
        self,
    ) -> None:
        """
        Initialize the service
        asynchronously.
        """


class HealthCheck(
    ABC,
):
    """
    Represents a service capable
    of reporting its health.
    """

    @abstractmethod
    def is_healthy(
        self,
    ) -> bool:
        """
        Return the current health
        status.
        """


class Startable(
    ABC,
):
    """
    Represents a service that
    participates in application
    startup.
    """

    @abstractmethod
    def start(
        self,
    ) -> None:
        """
        Start the service.
        """


class Stoppable(
    ABC,
):
    """
    Represents a service that
    participates in application
    shutdown.
    """

    @abstractmethod
    def stop(
        self,
    ) -> None:
        """
        Stop the service.
        """


__all__ = [
    "Service",
    "Disposable",
    "AsyncDisposable",
    "Initializable",
    "AsyncInitializable",
    "HealthCheck",
    "Startable",
    "Stoppable",
]
