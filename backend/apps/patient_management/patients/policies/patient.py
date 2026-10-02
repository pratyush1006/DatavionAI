"""
Patient Core authorization policy.

Authorization is delegated to the platform RBAC engine.

The Patient policy does not:
- query unrelated persistence,
- mutate models,
- implement HTTP behavior,
- bypass tenant boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.patient_management.patients.models import Patient
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines.permission import (
    user_has_permission,
)


@dataclass(
    frozen=True,
    slots=True,
)
class PatientPolicy:
    """
    Authorization policy for Patient Core.
    """

    @staticmethod
    def _check(
        *,
        actor: User,
        organization: Organization,
        permission: str,
    ) -> bool:
        """
        Evaluate a patient permission against an organization.
        """
        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_create(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="patients.create",
        )

    def can_view(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=organization,
            permission="patients.view",
        )

    def can_update(
        self,
        *,
        actor: User,
        patient: Patient,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=patient.organization,
            permission="patients.update",
        )

    def can_activate(
        self,
        *,
        actor: User,
        patient: Patient,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=patient.organization,
            permission="patients.activate",
        )

    def can_deactivate(
        self,
        *,
        actor: User,
        patient: Patient,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=patient.organization,
            permission="patients.deactivate",
        )

    def can_archive(
        self,
        *,
        actor: User,
        patient: Patient,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=patient.organization,
            permission="patients.archive",
        )

    def can_restore(
        self,
        *,
        actor: User,
        patient: Patient,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=patient.organization,
            permission="patients.restore",
        )

    def can_delete(
        self,
        *,
        actor: User,
        patient: Patient,
    ) -> bool:
        return self._check(
            actor=actor,
            organization=patient.organization,
            permission="patients.delete",
        )


__all__ = ("PatientPolicy",)
