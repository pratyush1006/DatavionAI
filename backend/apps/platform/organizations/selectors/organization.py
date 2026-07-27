"""
Read-only selectors for the Organizations application.

Selectors provide optimized read access for APIs,
dashboards, AI services, and platform workflows.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Final

from django.db.models import QuerySet
from django.shortcuts import get_object_or_404

from apps.platform.organizations.models import Organization

if TYPE_CHECKING:
    from apps.tenants.models import Tenant


type OrganizationQuerySet = QuerySet[Organization]


ORGANIZATION_LIST_FIELDS: Final[tuple[str, ...]] = (
    "id",
    "tenant",
    "name",
    "display_name",
    "slug",
    "code",
    "category",
    "organization_type",
    "organization_size",
    "status",
    "verification_status",
    "city",
    "state",
    "country",
    "is_active",
)


def get_organizations(
    *,
    include_inactive: bool = False,
    tenant: Tenant | Any | None = None,
    with_related: bool = False,
) -> OrganizationQuerySet:
    """
    Return organizations.

    Supports:

    - tenant isolation
    - inactive filtering
    - related-object optimization
    """

    queryset = Organization.objects.only(
        *ORGANIZATION_LIST_FIELDS,
    )

    if tenant is not None:
        queryset = queryset.for_tenant(
            tenant,
        )

    if not include_inactive:
        queryset = queryset.active()

    if with_related:
        queryset = queryset.with_related()

    return queryset


def get_active_organizations(
    *,
    tenant: Tenant | Any | None = None,
) -> OrganizationQuerySet:
    """
    Return active organizations.
    """

    return get_organizations(
        tenant=tenant,
    )


def get_verified_organizations(
    *,
    tenant: Tenant | Any | None = None,
) -> OrganizationQuerySet:
    """
    Return verified organizations.
    """

    return get_organizations(
        tenant=tenant,
        include_inactive=True,
    ).verified()


def get_organization_by_id(
    organization_id: Any,
    *,
    with_related: bool = False,
) -> Organization:
    """
    Return an organization by primary key.
    """

    return get_object_or_404(
        get_organizations(
            include_inactive=True,
            with_related=with_related,
        ),
        pk=organization_id,
    )


def get_organization_by_code(
    *,
    tenant: Tenant | Any,
    code: str,
) -> Organization:
    """
    Return an organization by tenant-scoped code.
    """

    code = code.strip().upper()

    return get_object_or_404(
        get_organizations(
            tenant=tenant,
            include_inactive=True,
        ),
        code=code,
    )


def get_organization_by_slug(
    *,
    tenant: Tenant | Any,
    slug: str,
) -> Organization:
    """
    Return an organization by tenant-scoped slug.
    """

    slug = slug.strip().lower()

    return get_object_or_404(
        get_organizations(
            tenant=tenant,
            include_inactive=True,
        ),
        slug=slug,
    )


def search_organizations(
    query: str,
    *,
    tenant: Tenant | Any | None = None,
) -> OrganizationQuerySet:
    """
    Search organizations.
    """

    return get_organizations(
        tenant=tenant,
        include_inactive=True,
    ).search(
        query,
    )


def organization_exists(
    *,
    tenant: Tenant | Any,
    code: str,
    include_inactive: bool = True,
) -> bool:
    """
    Check whether an organization exists.
    """

    code = code.strip().upper()

    return (
        get_organizations(
            tenant=tenant,
            include_inactive=include_inactive,
        )
        .filter(
            code=code,
        )
        .exists()
    )


def get_organization_summary(
    organization_id: Any,
) -> dict[str, Any]:
    """
    Return a lightweight organization summary.

    Used by:

    - dashboards
    - bootstrap APIs
    - AI context
    - navigation
    """

    organization = get_organization_by_id(
        organization_id,
    )

    return {
        "id": organization.id,
        "name": organization.name,
        "display_name": organization.display_name,
        "code": organization.code,
        "slug": organization.slug,
        "status": organization.status,
        "verification_status": organization.verification_status,
        "is_active": organization.is_active,
    }


__all__: tuple[str, ...] = (
    "OrganizationQuerySet",
    "get_active_organizations",
    "get_organization_by_code",
    "get_organization_by_id",
    "get_organization_by_slug",
    "get_organization_summary",
    "get_organizations",
    "get_verified_organizations",
    "organization_exists",
    "search_organizations",
)
