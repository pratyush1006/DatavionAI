"""
Audit queryset.
"""

from __future__ import annotations

from datetime import datetime

from django.db import models
from django.utils import timezone


class AuditQuerySet(
    models.QuerySet,
):
    """
    QuerySet for AuditLog.
    """

    def active(
        self,
    ):
        """
        Return active audit records.
        """

        return self.filter(
            is_active=True,
            is_deleted=False,
        )

    def for_organization(
        self,
        organization,
    ):
        """
        Filter by organization.
        """

        return self.filter(
            organization=organization,
        )

    def for_user(
        self,
        user,
    ):
        """
        Filter by user.
        """

        return self.filter(
            user=user,
        )

    def for_action(
        self,
        action: str,
    ):
        """
        Filter by audit action.
        """

        return self.filter(
            action=action,
        )

    def for_module(
        self,
        module: str,
    ):
        """
        Filter by module.
        """

        return self.filter(
            module=module,
        )

    def for_object(
        self,
        *,
        object_type: str,
        object_id: str,
    ):
        """
        Filter by audited object.
        """

        return self.filter(
            object_type=object_type,
            object_id=object_id,
        )

    def successful(
        self,
    ):
        """
        Return successful audit events.
        """

        return self.filter(
            success=True,
        )

    def failed(
        self,
    ):
        """
        Return failed audit events.
        """

        return self.filter(
            success=False,
        )

    def today(
        self,
    ):
        """
        Return today's audit events.
        """

        today = timezone.localdate()

        return self.filter(
            created_at__date=today,
        )

    def between(
        self,
        *,
        start: datetime,
        end: datetime,
    ):
        """
        Return audit events within a date range.
        """

        return self.filter(
            created_at__range=(
                start,
                end,
            ),
        )

    def recent(
        self,
    ):
        """
        Return newest audit events first.
        """

        return self.order_by(
            "-created_at",
        )

    def search(
        self,
        query: str,
    ):
        """
        Search audit events.
        """

        return self.filter(
            models.Q(
                object_id__icontains=query,
            )
            | models.Q(
                object_type__icontains=query,
            )
            | models.Q(
                module__icontains=query,
            )
            | models.Q(
                request_id__icontains=query,
            )
        )
