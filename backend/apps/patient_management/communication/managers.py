"""Managers and querysets for Patient Communication."""

from __future__ import annotations

from uuid import UUID

from apps.core.models.managers import SoftDeleteManager
from apps.core.models.querysets import SoftDeleteQuerySet


class CommunicationQuerySet(SoftDeleteQuerySet):
    """Provide reusable tenant and patient communication queries."""

    def for_patient(self, patient_id: UUID) -> CommunicationQuerySet:
        """Return communications for one patient."""
        return self.filter(patient_id=patient_id)

    def for_organization(self, organization_id: UUID) -> CommunicationQuerySet:
        """Return communications for one organization."""
        return self.filter(organization_id=organization_id)

    def by_status(self, status: str) -> CommunicationQuerySet:
        """Return communications with the requested status."""
        return self.filter(status=status)

    def by_channel(self, channel: str) -> CommunicationQuerySet:
        """Return communications on the requested channel."""
        return self.filter(channel=channel)


class CommunicationManager(SoftDeleteManager):
    """Default manager exposing only non-deleted communications."""

    def get_queryset(self) -> CommunicationQuerySet:
        """Return an alive communication queryset."""
        return CommunicationQuerySet(self.model, using=self._db).alive()


__all__ = ("CommunicationManager", "CommunicationQuerySet")
