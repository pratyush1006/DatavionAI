"""
Domain entity abstractions.
"""

from __future__ import annotations

from abc import (
    ABC,
    abstractmethod,
)
from typing import (
    Generic,
    TypeVar,
)

TIdentity = TypeVar("TIdentity")


class Entity(
    ABC,
    Generic[TIdentity],
):
    """
    Base class for all domain entities.
    """

    def __init__(
        self,
        identity: TIdentity,
    ) -> None:
        self._identity = identity

    @property
    def identity(
        self,
    ) -> TIdentity:
        """
        Return the entity identity.
        """
        return self._identity

    @property
    @abstractmethod
    def is_transient(
        self,
    ) -> bool:
        """
        Indicates whether the entity has a persistent identity.
        """

    def __eq__(
        self,
        other: object,
    ) -> bool:
        """
        Compare entities by identity.
        """
        if not isinstance(
            other,
            Entity,
        ):
            return False

        return type(self) is type(other) and self.identity == other.identity

    def __hash__(
        self,
    ) -> int:
        """
        Hash entity by type and identity.
        """
        return hash(
            (
                type(self),
                self.identity,
            ),
        )

    def __repr__(
        self,
    ) -> str:
        """
        Debug representation.
        """
        return f"{type(self).__name__}(identity={self.identity!r})"
