"""
Audit log model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel
from apps.platform.audit.constants import AuditAction
from apps.platform.audit.managers import AuditManager


class AuditLog(BaseModel):
    """
    Immutable audit log entry.

    Stores a complete audit trail for every
    business action performed within the platform.
    """

    objects = AuditManager()

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )

    action = models.CharField(
        max_length=20,
        choices=AuditAction.choices,
        db_index=True,
    )

    module = models.CharField(
        max_length=100,
        db_index=True,
    )

    object_type = models.CharField(
        max_length=100,
        db_index=True,
    )

    object_id = models.CharField(
        max_length=100,
        db_index=True,
    )

    old_values = models.JSONField(
        null=True,
        blank=True,
    )

    new_values = models.JSONField(
        null=True,
        blank=True,
    )

    request_id = models.CharField(
        max_length=100,
        blank=True,
        default="",
        db_index=True,
    )

    correlation_id = models.CharField(
        max_length=100,
        blank=True,
        default="",
        db_index=True,
    )

    session_key = models.CharField(
        max_length=100,
        blank=True,
        default="",
        db_index=True,
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
        default="",
    )

    http_method = models.CharField(
        max_length=10,
        blank=True,
        default="",
    )

    request_path = models.CharField(
        max_length=500,
        blank=True,
        default="",
    )

    status_code = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
    )

    success = models.BooleanField(
        default=True,
    )

    error_message = models.TextField(
        blank=True,
    )

    class Meta:
        """
        Django model metadata.
        """

        db_table = "audit_logs"

        verbose_name = "Audit Log"

        verbose_name_plural = "Audit Logs"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "created_at",
                ],
                name="audit_org_created_idx",
            ),
            models.Index(
                fields=[
                    "user",
                    "created_at",
                ],
                name="audit_user_created_idx",
            ),
            models.Index(
                fields=[
                    "action",
                    "created_at",
                ],
                name="audit_action_created_idx",
            ),
            models.Index(
                fields=[
                    "module",
                    "created_at",
                ],
                name="audit_module_created_idx",
            ),
            models.Index(
                fields=[
                    "object_type",
                    "object_id",
                ],
                name="audit_object_idx",
            ),
            models.Index(
                fields=[
                    "request_id",
                ],
                name="audit_request_idx",
            ),
            models.Index(
                fields=[
                    "correlation_id",
                ],
                name="audit_corr_idx",
            ),
            models.Index(
                fields=[
                    "session_key",
                ],
                name="audit_session_idx",
            ),
        ]

    @property
    def is_successful(
        self,
    ) -> bool:
        """
        Return whether the audited action succeeded.
        """

        return self.success

    def __str__(
        self,
    ) -> str:
        """
        Return a readable representation.
        """

        return f"{self.action} {self.module} ({self.created_at:%Y-%m-%d %H:%M:%S})"


__all__ = [
    "AuditLog",
]
