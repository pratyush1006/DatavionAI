"""
Publishable interface for the DatavionOS platform.

Defines the contract for resources that support publication
lifecycle management.

Used by:

- Documents
- Reports
- Templates
- Knowledge articles
- Clinical content
- AI generated assets
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol
from uuid import UUID


class Publishable(
    Protocol,
):
    """
    Contract for publishable resources.

    A publishable resource supports:

    - publication state tracking
    - publishing action
    - unpublishing action
    - publication audit metadata
    """

    @property
    def is_published(
        self,
    ) -> bool:
        """
        Return whether the resource is published.
        """
        ...

    @property
    def published_at(
        self,
    ) -> datetime | None:
        """
        Return publication timestamp.
        """
        ...

    @property
    def published_by_id(
        self,
    ) -> UUID | None:
        """
        Return identifier of the user who published
        the resource.
        """
        ...

    def publish(
        self,
        *,
        user_id: UUID | None = None,
    ) -> None:
        """
        Publish the resource.
        """
        ...

    def unpublish(
        self,
    ) -> None:
        """
        Remove publication status.
        """
        ...


__all__: tuple[str, ...] = ("Publishable",)
