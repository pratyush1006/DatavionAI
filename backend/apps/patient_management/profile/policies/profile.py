"""
Patient Profile authorization policies.

Uses the DatavionOS RBAC engine.

Authorization flow:

Workflow
    |
    v
ProfilePolicy
    |
    v
RBAC Engine
    |
    v
OrganizationRole + RolePermission
"""

from __future__ import annotations

from apps.patient_management.profile.models import (
    PatientProfile,
)
from apps.platform.accounts.models import (
    User,
)
from apps.platform.rbac.engines import (
    user_has_permission,
)


class ProfilePolicy:
    """
    Patient Profile authorization policy.

    Domain workflows must use the platform RBAC engine.
    """

    def can_create(
        self,
        *,
        actor: User,
        organization,
    ) -> bool:
        """
        Check profile creation permission.
        """

        return user_has_permission(
            user=actor,
            permission="patient_profile.create",
            organization=organization,
        )

    def can_manage(
        self,
        *,
        actor: User,
        profile: PatientProfile,
    ) -> bool:
        """
        Check profile update permission.
        """

        return user_has_permission(
            user=actor,
            permission="patient_profile.update",
            organization=profile.organization,
        )

    def can_delete(
        self,
        *,
        actor: User,
        profile: PatientProfile,
    ) -> bool:
        """
        Check profile deletion permission.
        """

        return user_has_permission(
            user=actor,
            permission="patient_profile.delete",
            organization=profile.organization,
        )

    def can_view(
        self,
        *,
        actor: User,
        profile: PatientProfile,
    ) -> bool:
        """
        Check profile view permission.
        """

        return user_has_permission(
            user=actor,
            permission="patient_profile.view",
            organization=profile.organization,
        )


__all__ = ("ProfilePolicy",)
