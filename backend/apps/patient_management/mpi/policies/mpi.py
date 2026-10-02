"""
Authorization policies for the Master Patient Index.
"""

from __future__ import annotations

from apps.platform.rbac.engines.permission import user_has_permission


class MPIPolicy:
    """Evaluate organization-scoped MPI permissions."""

    @staticmethod
    def _check(
        *,
        actor,
        permission: str,
        organization,
    ) -> bool:
        """Evaluate one RBAC permission."""

        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_list(self, *, actor, organization) -> bool:
        """Return whether the actor may list MPI records."""

        return self._check(
            actor=actor,
            permission="patient_mpi.list",
            organization=organization,
        )

    def can_view(self, *, actor, record) -> bool:
        """Return whether the actor may view an MPI record."""

        return self._check(
            actor=actor,
            permission="patient_mpi.view",
            organization=record.organization,
        )

    def can_create(self, *, actor, organization) -> bool:
        """Return whether the actor may create MPI records."""

        return self._check(
            actor=actor,
            permission="patient_mpi.create",
            organization=organization,
        )

    def can_update(self, *, actor, record) -> bool:
        """Return whether the actor may update an MPI record."""

        return self._check(
            actor=actor,
            permission="patient_mpi.update",
            organization=record.organization,
        )

    def can_delete(self, *, actor, record) -> bool:
        """Return whether the actor may delete an MPI record."""

        return self._check(
            actor=actor,
            permission="patient_mpi.delete",
            organization=record.organization,
        )

    def can_transition(self, *, actor, record) -> bool:
        """Return whether the actor may change MPI lifecycle state."""

        return self._check(
            actor=actor,
            permission="patient_mpi.transition",
            organization=record.organization,
        )

    def can_match(self, *, actor, organization) -> bool:
        """Return whether the actor may generate candidate matches."""

        return self._check(
            actor=actor,
            permission="patient_mpi.match",
            organization=organization,
        )

    def can_review(self, *, actor, candidate) -> bool:
        """Return whether the actor may review candidate matches."""

        return self._check(
            actor=actor,
            permission="patient_mpi.review",
            organization=candidate.organization,
        )

    def can_merge(self, *, actor, organization) -> bool:
        """Return whether the actor may merge MPI records."""

        return self._check(
            actor=actor,
            permission="patient_mpi.merge",
            organization=organization,
        )

    def can_reverse_merge(self, *, actor, record) -> bool:
        """Return whether the actor may reverse an MPI merge."""

        return self._check(
            actor=actor,
            permission="patient_mpi.reverse_merge",
            organization=record.organization,
        )

    def can_restore(self, *, actor, record) -> bool:
        """Return whether the actor may restore an MPI record."""

        return self._check(
            actor=actor,
            permission="patient_mpi.restore",
            organization=record.organization,
        )


__all__ = ("MPIPolicy",)
