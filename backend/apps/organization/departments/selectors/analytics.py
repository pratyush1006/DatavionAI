"""
Department analytics selectors.
"""

from __future__ import annotations

from django.db.models import Count

from apps.organization.departments.models import (
    Department,
)


class DepartmentAnalyticsSelector:
    """
    Department reporting queries.
    """

    @staticmethod
    def member_count(
        *,
        organization_id,
    ):

        return Department.objects.filter(
            organization_id=organization_id,
        ).annotate(
            total_members=Count(
                "members",
            )
        )


__all__ = ("DepartmentAnalyticsSelector",)
