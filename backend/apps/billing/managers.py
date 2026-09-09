"""
Billing Core query managers.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager


class BillingQuerySet(models.QuerySet):
    """Query helpers shared by Billing Core aggregates."""

    def for_organization(self, organization_id):
        """Limit records to one organization."""
        return self.filter(
            organization_id=organization_id,
        )


class BillingManager(BaseManager):
    """Default manager that excludes soft-deleted records."""

    def get_queryset(self):
        """Return live Billing Core records."""
        return (
            super()
            .get_queryset()
            .filter(
                is_deleted=False,
            )
        )


__all__ = (
    "BillingManager",
    "BillingQuerySet",
)
