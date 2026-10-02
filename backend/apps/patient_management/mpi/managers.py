"""
Querysets and managers for the Master Patient Index.
"""

from __future__ import annotations

from apps.core.models.managers import SoftDeleteManager
from apps.core.models.querysets import SoftDeleteQuerySet


class MPIRecordQuerySet(SoftDeleteQuerySet):
    """Query helpers for MPI records."""

    def active_records(self) -> MPIRecordQuerySet:
        """Return active MPI records."""

        return self.filter(status="ACTIVE", is_active=True)

    def by_organization(self, organization_id) -> MPIRecordQuerySet:
        """Return records belonging to one organization."""

        return self.filter(organization_id=organization_id)


class MPIRecordManager(
    SoftDeleteManager.from_queryset(MPIRecordQuerySet),
):
    """Default manager for alive MPI records."""


class MPIMatchQuerySet(SoftDeleteQuerySet):
    """Query helpers for MPI candidate matches."""

    def pending(self) -> MPIMatchQuerySet:
        """Return pending candidate matches."""

        return self.filter(status="PENDING")


class MPIMatchManager(
    SoftDeleteManager.from_queryset(MPIMatchQuerySet),
):
    """Default manager for alive MPI candidate matches."""


__all__ = (
    "MPIMatchManager",
    "MPIMatchQuerySet",
    "MPIRecordManager",
    "MPIRecordQuerySet",
)
