"""
Versionable interface for the DatavionOS platform.

Defines the contract for resources that maintain version history.

Used by:

- Clinical documents
- Consent forms
- Medical templates
- AI generated reports
- Knowledge assets
- Configuration artifacts
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol
from uuid import UUID


class Versionable(
    Protocol,
):
    """
    Contract for versioned resources.

    Versionable resources maintain a controlled lifecycle
    where changes create new versions rather than overwriting
    historical data.
    """

    @property
    def version(
        self,
    ) -> int:
        """
        Return current version number.
        """
        ...

    @property
    def previous_version_id(
        self,
    ) -> UUID | None:
        """
        Return identifier of previous version.
        """
        ...

    @property
    def version_created_at(
        self,
    ) -> datetime:
        """
        Return timestamp when current version was created.
        """
        ...

    @property
    def version_created_by_id(
        self,
    ) -> UUID | None:
        """
        Return user who created this version.
        """
        ...

    def create_new_version(
        self,
        *,
        user_id: UUID | None = None,
    ) -> None:
        """
        Create a new version of the resource.
        """
        ...


__all__: tuple[str, ...] = ("Versionable",)
