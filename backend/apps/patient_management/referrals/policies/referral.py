"""
Object and tenant policies for Patient Referrals.
"""

from __future__ import annotations

from apps.patient_management.referrals.permissions import (
    PatientReferralPermission,
)
from apps.platform.rbac.engines import user_has_permission


def _has_organization_membership(*, user, organization) -> bool:
    """Return whether the user has an active role in the organization."""

    return user.organization_roles.filter(
        organization_id=organization.id,
    ).exists()


class PatientReferralPolicy:
    """Centralize tenant and RBAC authorization decisions."""

    @staticmethod
    def can_list(*, user, organization) -> bool:
        """Return whether the user may list referrals."""

        return _has_organization_membership(
            user=user,
            organization=organization,
        ) and user_has_permission(
            user=user,
            permission=PatientReferralPermission.LIST,
            organization=organization,
        )

    @staticmethod
    def can_view(*, user, referral) -> bool:
        """Return whether the user may view a referral."""

        return _has_organization_membership(
            user=user,
            organization=referral.organization,
        ) and user_has_permission(
            user=user,
            permission=PatientReferralPermission.VIEW,
            organization=referral.organization,
        )

    @staticmethod
    def can_create(*, user, organization) -> bool:
        """Return whether the user may create referrals."""

        return _has_organization_membership(
            user=user,
            organization=organization,
        ) and user_has_permission(
            user=user,
            permission=PatientReferralPermission.CREATE,
            organization=organization,
        )

    @staticmethod
    def can_update(*, user, referral) -> bool:
        """Return whether the user may update a referral."""

        return _has_organization_membership(
            user=user,
            organization=referral.organization,
        ) and user_has_permission(
            user=user,
            permission=PatientReferralPermission.UPDATE,
            organization=referral.organization,
        )

    @staticmethod
    def can_delete(*, user, referral) -> bool:
        """Return whether the user may delete a referral."""

        return _has_organization_membership(
            user=user,
            organization=referral.organization,
        ) and user_has_permission(
            user=user,
            permission=PatientReferralPermission.DELETE,
            organization=referral.organization,
        )

    @staticmethod
    def can_restore(*, user, referral) -> bool:
        """Return whether the user may restore a referral."""

        return _has_organization_membership(
            user=user,
            organization=referral.organization,
        ) and user_has_permission(
            user=user,
            permission=PatientReferralPermission.RESTORE,
            organization=referral.organization,
        )

    @staticmethod
    def can_transition(*, user, referral) -> bool:
        """Return whether the user may transition a referral."""

        return _has_organization_membership(
            user=user,
            organization=referral.organization,
        ) and user_has_permission(
            user=user,
            permission=PatientReferralPermission.TRANSITION,
            organization=referral.organization,
        )


__all__ = ("PatientReferralPolicy",)
