"""
Team domain policies.

Contains business validation rules only.

Authorization is handled by RBAC.
"""

from __future__ import annotations


class TeamPolicy:
    """
    Business rules for Team operations.
    """

    @staticmethod
    def validate_organization(
        *,
        organization,
    ) -> bool:
        """
        Validate organization before creating a team.

        Domain rules:
        - organization must exist
        - organization must be active
        """

        return bool(organization and organization.is_active)

    @staticmethod
    def validate_organization_boundary(
        *,
        team,
        organization,
    ) -> bool:
        """
        Ensure team belongs to organization.
        """

        return team.organization_id == organization.id

    @staticmethod
    def validate_department_assignment(
        *,
        team,
        department,
    ) -> bool:
        """
        Ensure department belongs
        to the same organization as team.
        """

        return team.organization_id == department.organization_id

    @staticmethod
    def can_delete(
        *,
        team,
    ) -> bool:
        """
        Domain validation before deletion.

        Example:
        - prevent deletion of protected teams
        - prevent deletion with active members
        """

        return True


__all__ = ("TeamPolicy",)
