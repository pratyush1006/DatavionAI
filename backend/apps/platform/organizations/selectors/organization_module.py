"""
Read-only selectors for organization modules.

Selectors provide optimized read access for
organization module assignments.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import (
    OrganizationModule,
)

if TYPE_CHECKING:
    from apps.platform.organizations.models import (
        Organization,
    )


type OrganizationModuleQuerySet = QuerySet[OrganizationModule]


def get_modules(
    *,
    organization: Organization | Any | None = None,
    is_enabled: bool | None = None,
) -> OrganizationModuleQuerySet:
    """
    Return organization module assignments.
    """

    queryset = OrganizationModule.objects.select_related(
        "organization",
    )

    if organization is not None:
        queryset = queryset.filter(
            organization=organization,
        )

    if is_enabled is not None:
        queryset = queryset.filter(
            is_enabled=is_enabled,
        )

    return queryset


def get_module_by_id(
    module_id: Any,
) -> OrganizationModule:
    """
    Return a module assignment by primary key.
    """

    return get_object_or_404(
        get_modules(),
        pk=module_id,
    )


def get_organization_modules(
    organization: Organization | Any,
    *,
    enabled_only: bool = False,
) -> OrganizationModuleQuerySet:
    """
    Return module assignments for an organization.
    """

    return get_modules(
        organization=organization,
        is_enabled=True if enabled_only else None,
    )


def get_enabled_modules(
    organization: Organization | Any,
) -> OrganizationModuleQuerySet:
    """
    Return enabled module assignments.
    """

    return get_modules(
        organization=organization,
        is_enabled=True,
    )


def get_module_by_code(
    *,
    organization: Organization | Any,
    module_code: str,
) -> OrganizationModule:
    """
    Return a module assignment by module code.
    """

    return get_object_or_404(
        get_modules(
            organization=organization,
        ),
        module_code=module_code.strip().upper(),
    )


def module_exists(
    *,
    organization: Organization | Any,
    module_code: str,
) -> bool:
    """
    Check whether a module assignment exists.
    """

    return OrganizationModule.objects.filter(
        organization=organization,
        module_code=module_code.strip().upper(),
    ).exists()


__all__: tuple[str, ...] = (
    "OrganizationModuleQuerySet",
    "get_enabled_modules",
    "get_module_by_code",
    "get_module_by_id",
    "get_modules",
    "get_organization_modules",
    "module_exists",
)
