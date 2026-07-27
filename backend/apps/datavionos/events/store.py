"""
DatavionOS Event Store Contract.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Iterable

from apps.datavionos.events.event import (
    Event,
)


class EventStore(
    ABC,
):
    """
    Contract for append-only event stores.

    Implementations may use:

    - PostgreSQL
    - SQL Server
    - EventStoreDB
    - Cosmos DB
    - DynamoDB
    - MongoDB
    - Azure Table Storage
    """

    @property
    def store_name(
        self,
    ) -> str:
        """
        Store implementation name.
        """

        return self.__class__.__qualname__

    @property
    def supports_snapshots(
        self,
    ) -> bool:
        """
        Indicates whether snapshot
        persistence is supported.
        """

        return False

    @property
    def supports_replay(
        self,
    ) -> bool:
        """
        Indicates whether replay
        is supported.
        """

        return True

    @property
    def supports_concurrency(
        self,
    ) -> bool:
        """
        Indicates whether optimistic
        concurrency is supported.
        """

        return True

    @abstractmethod
    def append(
        self,
        event: Event,
    ) -> int:
        """
        Append an event.

        Returns
        -------
        int
            Stream version.
        """

    @abstractmethod
    def append_many(
        self,
        events: Iterable[Event,],
    ) -> tuple[
        int,
        ...,
    ]:
        """
        Append multiple events.

        Returns stream versions.
        """

    @abstractmethod
    def load_stream(
        self,
        aggregate_id: str,
    ) -> tuple[
        Event,
        ...,
    ]:
        """
        Load all events for an aggregate.
        """

    @abstractmethod
    def load_stream_from(
        self,
        aggregate_id: str,
        version: int,
    ) -> tuple[
        Event,
        ...,
    ]:
        """
        Load events beginning
        at a stream version.
        """

    @abstractmethod
    def load_by_correlation(
        self,
        correlation_id: str,
    ) -> tuple[
        Event,
        ...,
    ]:
        """
        Load correlated events.
        """

    @abstractmethod
    def load_by_causation(
        self,
        causation_id: str,
    ) -> tuple[
        Event,
        ...,
    ]:
        """
        Load causally-related events.
        """

    @abstractmethod
    def load_all(
        self,
    ) -> tuple[
        Event,
        ...,
    ]:
        """
        Load every stored event.
        """

    @abstractmethod
    def replay(
        self,
    ) -> Iterable[Event,]:
        """
        Replay all events in order.
        """

    @abstractmethod
    def current_version(
        self,
        aggregate_id: str,
    ) -> int:
        """
        Return aggregate version.
        """

    @abstractmethod
    def stream_exists(
        self,
        aggregate_id: str,
    ) -> bool:
        """
        Determine whether a stream exists.
        """

    @abstractmethod
    def delete_stream(
        self,
        aggregate_id: str,
    ) -> None:
        """
        Delete an aggregate stream.

        Primarily intended for
        development/testing.
        """

    def __repr__(
        self,
    ) -> str:
        """
        Developer representation.
        """

        return (
            f"{self.store_name}("
            f"snapshots={self.supports_snapshots}, "
            f"replay={self.supports_replay}, "
            f"concurrency={self.supports_concurrency})"
        )


__all__ = [
    "EventStore",
]
