"""
Organization role queryset.
"""

from __future__ import annotations

from django.db import models


class OrganizationRoleQuerySet(
    models.QuerySet,
):
    """
    QuerySet for OrganizationRole.
    """

    def active(
        self,
    ) -> OrganizationRoleQuerySet:
        """
        Return active organization roles.
        """

        return self.filter(
            is_active=True,
        )

    def inactive(
        self,
    ) -> OrganizationRoleQuerySet:
        """
        Return inactive organization roles.
        """

        return self.filter(
            is_active=False,
        )

    def for_organization(
        self,
        organization_id: int,
    ) -> OrganizationRoleQuerySet:
        """
        Filter by organization.
        """

        return self.filter(
            organization_id=organization_id,
        )

    def for_user(
        self,
        user_id: int,
    ) -> OrganizationRoleQuerySet:
        """
        Filter by user.
        """

        return self.filter(
            user_id=user_id,
        )

    def for_role(
        self,
        role_id: int,
    ) -> OrganizationRoleQuerySet:
        """
        Filter by role.
        """

        return self.filter(
            role_id=role_id,
        )

    def primary(
        self,
    ) -> OrganizationRoleQuerySet:
        """
        Return primary organization roles.
        """

        return self.filter(
            is_primary=True,
        )

    def with_related(
        self,
    ) -> OrganizationRoleQuerySet:
        """
        Select related objects.
        """

        return self.select_related(
            "organization",
            "user",
            "role",
        )

    def search(
        self,
        query: str,
    ) -> OrganizationRoleQuerySet:
        """
        Search organization role assignments.
        """

        if not query:
            return self

        return self.filter(
            models.Q(
                organization__name__icontains=query,
            )
            | models.Q(
                user__first_name__icontains=query,
            )
            | models.Q(
                user__last_name__icontains=query,
            )
            | models.Q(
                user__email__icontains=query,
            )
            | models.Q(
                role__name__icontains=query,
            )
        )


__all__ = [
    "OrganizationRoleQuerySet",
]
