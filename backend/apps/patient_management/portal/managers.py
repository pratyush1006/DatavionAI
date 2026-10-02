"""
Managers and querysets for Patient Portal accounts.
"""

from __future__ import annotations

from apps.core.models import SoftDeleteManager, SoftDeleteQuerySet


class PatientPortalAccountQuerySet(SoftDeleteQuerySet):
    """Queryset helpers for alive portal accounts."""

    def invited(self) -> PatientPortalAccountQuerySet:
        """Return invited accounts."""

        return self.filter(status="INVITED")

    def active(self) -> PatientPortalAccountQuerySet:
        """Return active accounts."""

        return self.filter(status="ACTIVE", is_active=True)

    def suspended(self) -> PatientPortalAccountQuerySet:
        """Return suspended accounts."""

        return self.filter(status="SUSPENDED")

    def locked(self) -> PatientPortalAccountQuerySet:
        """Return locked accounts."""

        return self.filter(status="LOCKED")

    def deactivated(self) -> PatientPortalAccountQuerySet:
        """Return deactivated accounts."""

        return self.filter(status="DEACTIVATED")


class PatientPortalAccountManager(
    SoftDeleteManager.from_queryset(PatientPortalAccountQuerySet)
):
    """Concrete migration-serializable manager class."""


__all__ = (
    "PatientPortalAccountManager",
    "PatientPortalAccountQuerySet",
)
