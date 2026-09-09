"""
Authorization policies for Patient Registration.

Authorization is delegated to the platform RBAC engine. The policy layer
contains no persistence mutation and does not implement HTTP behavior.
"""

from __future__ import annotations

from dataclasses import dataclass

from apps.patient_management.registration.models import PatientRegistration
from apps.platform.accounts.models import User
from apps.platform.organizations.models import Organization
from apps.platform.rbac.engines.permission import user_has_permission


@dataclass(frozen=True, slots=True)
class RegistrationPolicy:
    """Authorization policy for Patient Registration operations."""

    @staticmethod
    def _check(
        *,
        actor: User,
        organization: Organization,
        permission: str,
    ) -> bool:
        """Evaluate a registration permission through the RBAC engine."""
        return user_has_permission(
            user=actor,
            permission=permission,
            organization=organization,
        )

    def can_view(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """Return whether the actor may view registrations."""
        return self._check(
            actor=actor,
            organization=organization,
            permission="registrations.view",
        )

    def can_create(
        self,
        *,
        actor: User,
        organization: Organization,
    ) -> bool:
        """Return whether the actor may create registrations."""
        return self._check(
            actor=actor,
            organization=organization,
            permission="registrations.create",
        )

    def can_update(
        self,
        *,
        actor: User,
        registration: PatientRegistration,
    ) -> bool:
        """Return whether the actor may update a registration."""
        return self._check(
            actor=actor,
            organization=registration.organization,
            permission="registrations.update",
        )

    def can_verify(
        self,
        *,
        actor: User,
        registration: PatientRegistration,
    ) -> bool:
        """Return whether the actor may verify a registration."""
        return self._check(
            actor=actor,
            organization=registration.organization,
            permission="registrations.verify",
        )

    def can_check_in(
        self,
        *,
        actor: User,
        registration: PatientRegistration,
    ) -> bool:
        """Return whether the actor may check in a registration."""
        return self._check(
            actor=actor,
            organization=registration.organization,
            permission="registrations.check_in",
        )

    def can_complete(
        self,
        *,
        actor: User,
        registration: PatientRegistration,
    ) -> bool:
        """Return whether the actor may complete a registration."""
        return self._check(
            actor=actor,
            organization=registration.organization,
            permission="registrations.complete",
        )

    def can_cancel(
        self,
        *,
        actor: User,
        registration: PatientRegistration,
    ) -> bool:
        """Return whether the actor may cancel a registration."""
        return self._check(
            actor=actor,
            organization=registration.organization,
            permission="registrations.cancel",
        )

    def can_reject(
        self,
        *,
        actor: User,
        registration: PatientRegistration,
    ) -> bool:
        """Return whether the actor may reject a registration."""
        return self._check(
            actor=actor,
            organization=registration.organization,
            permission="registrations.reject",
        )

    def can_no_show(
        self,
        *,
        actor: User,
        registration: PatientRegistration,
    ) -> bool:
        """Return whether the actor may mark a registration as no-show."""
        return self._check(
            actor=actor,
            organization=registration.organization,
            permission="registrations.no_show",
        )

    def can_delete(
        self,
        *,
        actor: User,
        registration: PatientRegistration,
    ) -> bool:
        """Return whether the actor may delete a registration."""
        return self._check(
            actor=actor,
            organization=registration.organization,
            permission="registrations.delete",
        )


__all__ = ("RegistrationPolicy",)
