"""
Identifiable interface for the DatavionOS platform.

Defines the contract for objects that expose a globally unique
identifier.

This interface is framework agnostic and can be implemented by:

- Django models
- Domain entities
- DTOs
- External integration objects
"""

from __future__ import annotations

from typing import Protocol
from uuid import UUID


class Identifiable(
    Protocol,
):
    """
    Contract for objects exposing a unique identifier.

    The identifier should be:

    - globally unique
    - immutable
    - stable across the object's lifecycle
    - suitable for distributed systems

    Typical implementation:

        class Organization(BaseModel):

            @property
            def identifier(self) -> UUID:
                return self.id
    """

    @property
    def identifier(
        self,
    ) -> UUID:
        """
        Return the unique identifier.

        Returns:
            UUID identifier.
        """
        ...


__all__: tuple[str, ...] = ("Identifiable",)
