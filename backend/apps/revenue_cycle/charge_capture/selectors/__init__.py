"""Read selectors for Charge Capture."""

from __future__ import annotations

from uuid import UUID

from ..models import Charge

__all__ = ("ChargeSelector",)


class ChargeSelector:
    """Provide tenant-scoped read access to charges."""

    @staticmethod
    def get(*, charge_id: UUID, tenant_id: UUID, organization_id: UUID) -> Charge:
        """Return one active charge inside the supplied scope."""

        return Charge.objects.select_related(
            "patient",
            "organization",
        ).get(
            id=charge_id,
            tenant_id=tenant_id,
            organization_id=organization_id,
            is_deleted=False,
        )

    @staticmethod
    def list(*, tenant_id: UUID, organization_id: UUID):
        """Return active charges inside the supplied scope."""

        return Charge.objects.select_related(
            "patient",
            "organization",
        ).filter(
            tenant_id=tenant_id,
            organization_id=organization_id,
            is_deleted=False,
        )
