"""Organization-scoped selectors for Revenue Cycle integration records."""

from __future__ import annotations

from uuid import UUID

from django.db.models import QuerySet

from .models import RevenueCycleIntegrationRecord


class CrossModuleIntegrationSelector:
    """Provide organization-scoped integration record reads."""

    @staticmethod
    def records(
        *,
        organization_id: UUID,
        status: str | None = None,
        source: str | None = None,
    ) -> QuerySet[RevenueCycleIntegrationRecord]:
        """Return filtered integration records."""

        queryset = RevenueCycleIntegrationRecord.objects.filter(
            organization_id=organization_id,
        )
        if status:
            queryset = queryset.filter(status=status)
        if source:
            queryset = queryset.filter(source=source)
        return queryset.order_by("-created_at")


__all__ = ("CrossModuleIntegrationSelector",)
