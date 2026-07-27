"""
Permission test factories.

Creates RBAC permissions for testing.

Permission code convention:

    module.action

Examples:

    rbac.create
    patients.view
    appointments.update

Scope is stored separately and is NOT part
of the permission code.
"""

from __future__ import annotations

import factory

from apps.platform.rbac.builders import (
    PermissionBuilder,
)
from apps.platform.rbac.constants import (
    PermissionAction,
    PermissionModule,
    PermissionScope,
)
from apps.platform.rbac.models import (
    Permission,
)


class PermissionFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for Permission.
    """

    class Meta:
        model = Permission

    # =========================================================================
    # Defaults
    # =========================================================================

    module = PermissionModule.PATIENTS

    scope = PermissionScope.ORGANIZATION

    action = factory.Sequence(
        lambda n: [
            PermissionAction.VIEW,
            PermissionAction.CREATE,
            PermissionAction.UPDATE,
            PermissionAction.DELETE,
            PermissionAction.APPROVE,
            PermissionAction.ASSIGN,
            PermissionAction.VERIFY,
            PermissionAction.RELEASE,
            PermissionAction.SIGN,
            PermissionAction.UPLOAD,
            PermissionAction.DOWNLOAD,
            PermissionAction.EXPORT,
            PermissionAction.IMPORT,
            PermissionAction.SHARE,
            PermissionAction.PRINT,
        ][n % 15],
    )

    description = factory.Faker(
        "sentence",
    )

    display_order = factory.Sequence(
        lambda n: n,
    )

    is_system = True

    is_assignable = True

    is_delegable = False

    is_active = True

    # =========================================================================
    # Generated fields
    # =========================================================================

    @factory.lazy_attribute
    def code(
        self,
    ) -> str:
        """
        Generate permission code.

        Scope is not included.

        Example:

            rbac.create

        not:

            rbac.create.organization
        """

        return PermissionBuilder.build(
            module=self.module,
            action=self.action,
        )

    @factory.lazy_attribute
    def name(
        self,
    ) -> str:
        """
        Generate permission display name.
        """

        return PermissionBuilder.build_name(
            module=self.module,
            action=self.action,
            scope=self.scope,
        )


# ============================================================================
# Backward compatibility helpers
# ============================================================================


def create_permission(
    **kwargs,
) -> Permission:
    """
    Create permission.
    """

    return PermissionFactory(
        **kwargs,
    )


def create_system_permission(
    **kwargs,
) -> Permission:
    """
    Create system permission.
    """

    kwargs.setdefault(
        "is_system",
        True,
    )

    return PermissionFactory(
        **kwargs,
    )


__all__ = [
    "PermissionFactory",
    "create_permission",
    "create_system_permission",
]
