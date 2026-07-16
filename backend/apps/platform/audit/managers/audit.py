"""
Audit manager.
"""

from __future__ import annotations

from django.db import models

from apps.platform.audit.querysets import AuditQuerySet


class AuditManager(
    models.Manager.from_queryset(
        AuditQuerySet,
    ),
):
    """
    Manager for AuditLog.
    """

    def get_queryset(
        self,
    ) -> AuditQuerySet:
        """
        Return the default queryset.
        """

        return super().get_queryset()

    def active(
        self,
    ) -> AuditQuerySet:
        """
        Return active audit records.
        """

        return self.get_queryset().active()

    def recent(
        self,
    ) -> AuditQuerySet:
        """
        Return recent audit records.
        """

        return self.get_queryset().recent()

    def successful(
        self,
    ) -> AuditQuerySet:
        """
        Return successful audit records.
        """

        return self.get_queryset().successful()

    def failed(
        self,
    ) -> AuditQuerySet:
        """
        Return failed audit records.
        """

        return self.get_queryset().failed()
