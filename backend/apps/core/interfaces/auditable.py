"""
Auditable interface for the DatavionOS platform.

Defines the contract for objects that maintain audit ownership
information.

Used by healthcare, financial, and compliance-sensitive domains.

Examples:

- Patient records
- Clinical documents
- Consent records
- Billing transactions
- Audit events
"""

from __future__ import annotations

from datetime import datetime
from typing import Protocol
from uuid import UUID


class Auditable(
    Protocol,
):
    """
    Contract for objects supporting audit metadata.

    Implementations should expose:

    - creator identity
    - last modifier identity
    - creation timestamp
    - modification timestamp

    This interface is intentionally framework agnostic.
    """

    @property
    def created_by_id(
        self,
    ) -> UUID | None:
        """
        Return the creator identifier.
        """
        ...

    @property
    def updated_by_id(
        self,
    ) -> UUID | None:
        """
        Return the last modifier identifier.
        """
        ...

    @property
    def created_at(
        self,
    ) -> datetime:
        """
        Return creation timestamp.
        """
        ...

    @property
    def updated_at(
        self,
    ) -> datetime:
        """
        Return modification timestamp.
        """
        ...


__all__: tuple[str, ...] = ("Auditable",)
