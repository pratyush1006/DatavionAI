"""
Audit log model.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models

from apps.core.models import BaseModel


class AuditLog(BaseModel):
    """
    Immutable audit log entry.

    Records business actions performed within the platform.
    """

    ACTION_CHOICES = (
        ("CREATE", "Create"),
        ("UPDATE", "Update"),
        ("DELETE", "Delete"),
        ("LOGIN", "Login"),
        ("LOGOUT", "Logout"),
        ("APPROVE", "Approve"),
        ("REJECT", "Reject"),
        ("EXPORT", "Export"),
        ("IMPORT", "Import"),
    )

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
        choices=ACTION_CHOICES,
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
    )

    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True,
    )

    user_agent = models.TextField(
        blank=True,
        default="",
    )

    class Meta:
        db_table = "audit_logs"
        ordering = ("-created_at",)
        indexes = [
            models.Index(
                fields=[
                    "action",
                    "created_at",
                ],
            ),
            models.Index(
                fields=[
                    "module",
                    "created_at",
                ],
            ),
            models.Index(
                fields=[
                    "object_type",
                    "object_id",
                ],
            ),
        ]

    def __str__(self) -> str:
        return f"{self.action} {self.module} ({self.created_at:%Y-%m-%d %H:%M:%S})"
