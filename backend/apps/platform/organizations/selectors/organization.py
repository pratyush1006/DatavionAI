"""
Read-only selectors for the Organizations application.

Selectors provide optimized read access for APIs,
dashboards, AI services, and platform workflows.

Security
--------
Tenant-aware callers must provide ``tenant`` when resolving an
organization. Tenant isolation is enforced at the queryset level
before object-level RBAC permissions are evaluated.
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
    "size",
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

    Args:
        include_inactive:
            Include inactive organizations when True.

        tenant:
            Optional tenant context. When supplied, the queryset is
            strictly scoped to that tenant.

        with_related:
            Load related objects using the organization's queryset
            optimization method.
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
        include_inactive=False,
    )


def get_verified_organizations(
    *,
    tenant: Tenant | Any | None = None,
) -> OrganizationQuerySet:
    """
    Return verified organizations.

    Inactive organizations are included because verification status
    and lifecycle status are independent concerns.
    """

    return get_organizations(
        tenant=tenant,
        include_inactive=True,
    ).verified()


def get_organization_by_id(
    organization_id: Any,
    *,
    tenant: Tenant | Any | None = None,
    with_related: bool = False,
) -> Organization:
    """
    Return an organization by primary key.

    When ``tenant`` is supplied, the lookup is strictly scoped to
    that tenant.

    This provides tenant isolation at the database-query level before
    object-level RBAC permissions are evaluated.

    Inactive organizations are intentionally included because detail,
    update, delete, restore, and lifecycle operations may need to
    resolve inactive organizations.
    """

    queryset = get_organizations(
        tenant=tenant,
        include_inactive=True,
        with_related=with_related,
    )

    return get_object_or_404(
        queryset,
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

    normalized_code = code.strip().upper()

    return get_object_or_404(
        get_organizations(
            tenant=tenant,
            include_inactive=True,
        ),
        code=normalized_code,
    )


def get_organization_by_slug(
    *,
    tenant: Tenant | Any,
    slug: str,
) -> Organization:
    """
    Return an organization by tenant-scoped slug.
    """

    normalized_slug = slug.strip().lower()

    return get_object_or_404(
        get_organizations(
            tenant=tenant,
            include_inactive=True,
        ),
        slug=normalized_slug,
    )


def search_organizations(
    query: str,
    *,
    tenant: Tenant | Any | None = None,
) -> OrganizationQuerySet:
    """
    Search organizations.

    Search remains tenant-scoped whenever a tenant is supplied.
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
    Check whether an organization code exists within a tenant.
    """

    normalized_code = code.strip().upper()

    return (
        get_organizations(
            tenant=tenant,
            include_inactive=include_inactive,
        )
        .filter(
            code=normalized_code,
        )
        .exists()
    )


def get_organization_summary(
    organization_id: Any,
    *,
    tenant: Tenant | Any | None = None,
) -> dict[str, Any]:
    """
    Return a lightweight organization summary.

    Used by:

    - dashboards
    - bootstrap APIs
    - AI context
    - navigation

    Tenant context is propagated to prevent an organization outside
    the active tenant boundary from being resolved accidentally.
    """

    organization = get_organization_by_id(
        organization_id,
        tenant=tenant,
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
