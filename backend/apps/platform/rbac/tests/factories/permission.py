"""
Permission test factories.
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
        Generate the permission code.
        """

        return PermissionBuilder.build(
            module=self.module,
            action=self.action,
            scope=self.scope,
        )

    @factory.lazy_attribute
    def name(
        self,
    ) -> str:
        """
        Generate the permission name.
        """

        return PermissionBuilder.build_name(
            module=self.module,
            action=self.action,
            scope=self.scope,
        )


# ============================================================================
# Backward compatibility
# ============================================================================


def create_permission(
    **kwargs,
) -> Permission:
    """
    Backward-compatible helper.
    """

    return PermissionFactory(
        **kwargs,
    )


def create_system_permission(
    **kwargs,
) -> Permission:
    """
    Create a built-in system permission.
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
