"""
Authorization policy for Patient Timeline.

Authorization is delegated to the platform RBAC engine.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.patient_management.timeline.models import TimelineEntry
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines.permission import user_has_permission


@dataclass(
    frozen=True,
    slots=True,
)
class TimelinePolicy:
    """Evaluate organization-scoped Timeline permissions."""

    @staticmethod
    def _check(
        *,
        actor: User,
        permission: str,
        organization: Organization,
    ) -> bool:
        """Evaluate one permission through the platform RBAC engine."""

        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_view(
        self,
        *,
        actor: User,
        entry: TimelineEntry,
    ) -> bool:
        """Check Timeline view permission."""

        return self._check(
            actor=actor,
            permission="patient_timeline.view",
            organization=entry.organization,
        )

    def can_list(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """Check Timeline list permission."""

        return self._check(
            actor=actor,
            permission="patient_timeline.list",
            organization=organization,
        )

    def can_create(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """Check Timeline creation permission."""

        return self._check(
            actor=actor,
            permission="patient_timeline.create",
            organization=organization,
        )

    def can_update(
        self,
        *,
        actor: User,
        entry: TimelineEntry,
    ) -> bool:
        """Check Timeline update permission."""

        return self._check(
            actor=actor,
            permission="patient_timeline.update",
            organization=entry.organization,
        )

    def can_delete(
        self,
        *,
        actor: User,
        entry: TimelineEntry,
    ) -> bool:
        """Check Timeline deletion permission."""

        return self._check(
            actor=actor,
            permission="patient_timeline.delete",
            organization=entry.organization,
        )

    def can_restore(
        self,
        *,
        actor: User,
        entry: TimelineEntry,
    ) -> bool:
        """Check Timeline restore permission."""

        return self._check(
            actor=actor,
            permission="patient_timeline.restore",
            organization=entry.organization,
        )

    def can_activate(
        self,
        *,
        actor: User,
        entry: TimelineEntry,
    ) -> bool:
        """Check Timeline activation permission."""

        return self._check(
            actor=actor,
            permission="patient_timeline.activate",
            organization=entry.organization,
        )

    def can_deactivate(
        self,
        *,
        actor: User,
        entry: TimelineEntry,
    ) -> bool:
        """Check Timeline deactivation permission."""

        return self._check(
            actor=actor,
            permission="patient_timeline.deactivate",
            organization=entry.organization,
        )

    def can_archive(
        self,
        *,
        actor: User,
        entry: TimelineEntry,
    ) -> bool:
        """Check Timeline archival permission."""

        return self._check(
            actor=actor,
            permission="patient_timeline.archive",
            organization=entry.organization,
        )


__all__ = ("TimelinePolicy",)
