"""Tenant-safe selectors for claim scrubbing."""

from __future__ import annotations

from django.db.models import QuerySet

from apps.revenue_cycle.claim_scrubbing.models import ClaimScrub, ScrubRule


def list_scrubs(*, organization_id: str, tenant_id: str) -> QuerySet[ClaimScrub]:
    """Return active scrubs for an organization inside its tenant."""

    return ClaimScrub.objects.filter(
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    ).select_related("patient", "organization")


def get_scrub(*, organization_id: str, tenant_id: str, scrub_id: str) -> ClaimScrub:
    """Return one tenant-scoped scrub."""

    return list_scrubs(organization_id=organization_id, tenant_id=tenant_id).get(
        id=scrub_id
    )


def get_scrub_for_update(
    *, organization_id: str, tenant_id: str, scrub_id: str
) -> ClaimScrub:
    """Return one tenant-scoped scrub with a row lock."""

    return (
        list_scrubs(organization_id=organization_id, tenant_id=tenant_id)
        .select_for_update()
        .get(id=scrub_id)
    )


def list_active_rules(*, organization_id: str, tenant_id: str) -> QuerySet[ScrubRule]:
    """Return active rules for an organization inside its tenant."""

    return ScrubRule.objects.filter(
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
        is_active=True,
    ).order_by("priority", "code")


__all__ = ("list_scrubs", "get_scrub", "get_scrub_for_update", "list_active_rules")
