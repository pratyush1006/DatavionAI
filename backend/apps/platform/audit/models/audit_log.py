"""
Audit log model.

Enterprise audit trail for DatavionOS.

Supports:

- Multi-tenant SaaS isolation
- Organization tracking
- User activity tracking
- Healthcare PHI auditing
- Security compliance
- Immutable append-only records
"""

from __future__ import annotations

from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q

from apps.core.models import BaseModel
from apps.platform.audit.constants import (
    AuditAction,
)
from apps.platform.audit.managers import (
    AuditManager,
)


class AuditLog(
    BaseModel,
):
    """
    Immutable audit log entry.

    Every important platform action
    creates an audit record.

    Audit hierarchy:

        Tenant
            |
        Organization
            |
        User
            |
        Action
            |
        Resource
    """

    objects = AuditManager()

    # ======================================================================
    # Ownership / Tenant Context
    # ======================================================================

    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
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

    # ======================================================================
    # Audit Event
    # ======================================================================

    action = models.CharField(
        max_length=30,
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

    # ======================================================================
    # Data Snapshot
    # ======================================================================

    old_values = models.JSONField(
        null=True,
        blank=True,
    )

    new_values = models.JSONField(
        null=True,
        blank=True,
    )

    # ======================================================================
    # Request / Security Context
    # ======================================================================

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

    # ======================================================================
    # Execution Result
    # ======================================================================

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
        Django metadata.
        """

        db_table = "audit_logs"

        verbose_name = "Audit Log"

        verbose_name_plural = "Audit Logs"

        ordering = ("-created_at",)

        indexes = [
            models.Index(
                fields=[
                    "tenant",
                    "created_at",
                ],
                name="audit_tenant_created_idx",
            ),
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
        ]

        constraints = [
            models.CheckConstraint(
                condition=~Q(
                    module="",
                ),
                name="audit_module_required",
            ),
            models.CheckConstraint(
                condition=~Q(
                    object_type="",
                ),
                name="audit_object_type_required",
            ),
        ]

    # ======================================================================
    # Properties
    # ======================================================================

    @property
    def is_successful(
        self,
    ) -> bool:
        """
        Return execution status.
        """

        return self.success

    # ======================================================================
    # Immutable Protection
    # ======================================================================

    def save(
        self,
        *args,
        **kwargs,
    ):
        """
        Audit logs are append-only.

        Existing records cannot be modified.
        """

        if self.pk:
            exists = (
                type(self)
                .objects.filter(
                    pk=self.pk,
                )
                .exists()
            )

            if exists:
                raise ValidationError(
                    "Audit logs are immutable and cannot be modified.",
                )

        return super().save(
            *args,
            **kwargs,
        )

    def delete(
        self,
        *args,
        **kwargs,
    ):
        """
        Audit logs cannot be deleted.

        Required for:

        - HIPAA compliance
        - SOC2 compliance
        - ISO 27001 auditability
        """

        raise ValidationError(
            "Audit logs cannot be deleted.",
        )

    # ======================================================================
    # Representation
    # ======================================================================

    def __str__(
        self,
    ) -> str:

        return f"{self.action} {self.module} ({self.created_at:%Y-%m-%d %H:%M:%S})"


__all__ = [
    "AuditLog",
]
