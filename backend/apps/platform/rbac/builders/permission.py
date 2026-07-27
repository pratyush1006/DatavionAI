"""
Permission builder.

Responsible for generating standardized permission codes
and display names.
"""

from __future__ import annotations


class PermissionBuilder:
    """
    Builds standardized permission codes.
    """

    @staticmethod
    def build(
        *,
        module: str,
        action: str,
    ) -> str:
        """
        Build a permission code.

        Permission codes are scope independent.

        Examples:

            patients.view
            rbac.create
        """

        return ".".join(
            (
                module,
                action,
            )
        ).lower()

    @staticmethod
    def build_name(
        *,
        action: str,
        module: str,
        scope: str | None = None,
    ) -> str:
        """
        Build a human-readable permission name.

        Example:

            View Patients (Organization)
        """

        name = f"{action.replace('_', ' ').title()} {module.replace('_', ' ').title()}"

        if scope:
            name += f" ({scope.replace('_', ' ').title()})"

        return name


__all__ = [
    "PermissionBuilder",
]
