"""
Factories for PermissionGroup tests.
"""

from __future__ import annotations

import factory

from apps.platform.rbac.builders import (
    PermissionGroupBuilder,
)
from apps.platform.rbac.constants import (
    PermissionModule,
)
from apps.platform.rbac.models import (
    PermissionGroup,
)


class PermissionGroupFactory(
    factory.django.DjangoModelFactory,
):
    """
    Factory for PermissionGroup.
    """

    class Meta:
        """
        Factory configuration.
        """

        model = PermissionGroup

    name = factory.Sequence(
        lambda n: f"Permission Group {n}",
    )

    module = PermissionModule.PATIENTS

    description = factory.Faker(
        "sentence",
    )

    display_order = factory.Sequence(
        lambda n: n,
    )

    is_system = True

    is_active = True

    @factory.lazy_attribute
    def code(
        self,
    ) -> str:
        """
        Generate the permission group code.
        """

        return PermissionGroupBuilder.build_code(
            name=self.name,
        )


__all__ = [
    "PermissionGroupFactory",
]
