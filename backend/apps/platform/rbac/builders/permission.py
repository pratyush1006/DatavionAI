"""
Permission builder.

Responsible for generating standardized permission codes.
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
        scope: str,
    ) -> str:
        """
        Build a permission code.

        Example:
            patients.view.self
        """

        return ".".join(
            (
                module,
                action,
                scope,
            )
        )

    @staticmethod
    def build_name(
        *,
        action: str,
        module: str,
        scope: str,
    ) -> str:
        """
        Build a human-readable permission name.

        Example:
            View Patients (Organization)
        """

        return (
            f"{action.replace('_', ' ').title()} "
            f"{module.replace('_', ' ').title()} "
            f"({scope.replace('_', ' ').title()})"
        )


__all__ = [
    "PermissionBuilder",
]
