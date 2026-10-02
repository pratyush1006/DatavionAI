"""
DatavionOS Search API Filters.

Tenant aware search filtering.
"""

from __future__ import annotations

from typing import Any


class SearchFilterSet:
    """
    Search filter helper.
    """

    @staticmethod
    def build(
        *,
        tenant_id: str | None = None,
        organization_id: str | None = None,
        patient_id: str | None = None,
    ) -> dict[str, Any]:
        """
        Build search filters.
        """

        return {
            key: value
            for key, value in {
                "tenant_id": tenant_id,
                "organization_id": organization_id,
                "patient_id": patient_id,
            }.items()
            if value is not None
        }


__all__ = ("SearchFilterSet",)
