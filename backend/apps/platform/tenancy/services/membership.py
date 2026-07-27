"""
Tenant membership services.

Handles tenant-user lifecycle operations.
"""

from __future__ import annotations

from django.contrib.auth import get_user_model

from apps.platform.tenancy.models import (
    Tenant,
    TenantMembership,
)

User = get_user_model()


class TenantMembershipService:
    """
    Business logic for tenant memberships.
    """

    @staticmethod
    def create_membership(
        *,
        tenant: Tenant,
        user: User,
        is_owner: bool = False,
    ) -> TenantMembership:
        """
        Create or restore tenant membership.
        """

        membership, _ = TenantMembership.objects.get_or_create(
            tenant=tenant,
            user=user,
            defaults={
                "is_owner": is_owner,
                "status": (TenantMembership.Status.ACTIVE),
            },
        )

        if membership.status != (TenantMembership.Status.ACTIVE):
            membership.status = TenantMembership.Status.ACTIVE

            membership.is_owner = is_owner

            membership.save(
                update_fields=[
                    "status",
                    "is_owner",
                    "updated_at",
                ],
            )

        return membership

    @staticmethod
    def activate_membership(
        membership: TenantMembership,
    ) -> TenantMembership:
        """
        Activate membership.
        """

        membership.status = TenantMembership.Status.ACTIVE

        membership.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return membership

    @staticmethod
    def suspend_membership(
        membership: TenantMembership,
    ) -> TenantMembership:
        """
        Suspend membership.
        """

        membership.status = TenantMembership.Status.SUSPENDED

        membership.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return membership

    @staticmethod
    def remove_membership(
        membership: TenantMembership,
    ) -> TenantMembership:
        """
        Remove membership.
        """

        membership.status = TenantMembership.Status.REMOVED

        membership.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return membership


__all__ = ("TenantMembershipService",)
