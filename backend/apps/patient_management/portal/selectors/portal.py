"""
Read-only selectors for Patient Portal accounts.
"""

from __future__ import annotations

from uuid import UUID

from apps.patient_management.portal.models import PatientPortalAccount


def list_portal_accounts(
    *,
    tenant_id: UUID,
    organization_id: UUID,
):
    """Return alive portal accounts inside one tenant and organization."""

    return (
        PatientPortalAccount.objects.filter(
            organization_id=organization_id,
            organization__tenant_id=tenant_id,
        )
        .select_related("organization", "patient")
        .order_by("username")
    )


def get_portal_account(
    *,
    tenant_id: UUID,
    organization_id: UUID,
    account_id: UUID,
) -> PatientPortalAccount:
    """Return one alive portal account within the requested boundary."""

    return PatientPortalAccount.objects.select_related("organization", "patient").get(
        pk=account_id,
        organization_id=organization_id,
        organization__tenant_id=tenant_id,
    )


__all__ = (
    "get_portal_account",
    "list_portal_accounts",
)
