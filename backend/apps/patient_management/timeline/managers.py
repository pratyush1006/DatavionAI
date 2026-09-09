"""
Query managers for Patient Timeline.

Timeline uses the platform soft-delete manager while exposing
Timeline-specific query helpers through a specialized queryset.
"""

from __future__ import annotations

from uuid import UUID

from apps.core.models import SoftDeleteManager, SoftDeleteQuerySet


class TimelineEntryQuerySet(SoftDeleteQuerySet):
    """Provide reusable TimelineEntry queryset operations."""

    def active(self) -> TimelineEntryQuerySet:
        """Return alive Timeline entries in the active domain state."""

        return self.alive().filter(
            is_active=True,
            status="active",
        )

    def inactive(self) -> TimelineEntryQuerySet:
        """Return alive Timeline entries in the inactive domain state."""

        return self.alive().filter(
            is_active=False,
        )

    def for_patient(
        self,
        patient_id: UUID,
    ) -> TimelineEntryQuerySet:
        """Return alive entries belonging to the supplied patient."""

        return self.alive().filter(
            patient_id=patient_id,
        )

    def for_organization(
        self,
        organization_id: UUID,
    ) -> TimelineEntryQuerySet:
        """Return alive entries belonging to the supplied organization."""

        return self.alive().filter(
            organization_id=organization_id,
        )

    def current(self) -> TimelineEntryQuerySet:
        """Return alive and active Timeline entries."""

        return self.active()


class TimelineEntryManager(SoftDeleteManager):
    """Expose alive Timeline entries through the platform soft-delete manager."""

    def get_queryset(self) -> TimelineEntryQuerySet:
        """Return the Timeline queryset scoped to non-deleted records."""

        return TimelineEntryQuerySet(
            self.model,
            using=self._db,
        ).alive()


__all__ = (
    "TimelineEntryManager",
    "TimelineEntryQuerySet",
)
