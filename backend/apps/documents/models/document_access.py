"""
Document access model.

Controls document access permissions.

Responsibilities
----------------
- User access management
- Permission assignment
- Access lifecycle
- Expiry handling

Non-responsibilities
--------------------
- Authentication
- RBAC role definition
- Tenant membership

Those belong to:
- accounts
- RBAC bounded context
- tenancy
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import (
    BaseModel,
)
from apps.documents.constants import (
    DocumentPermission,
)


class DocumentAccess(
    BaseModel,
):
    """
    Represents access granted to a user for a document.

    Example:

        Document
            |
            +-- DocumentAccess
                    |
                    +-- User
                    |
                    +-- Permission
    """

    # ============================================================
    # Relationship
    # ============================================================

    document = models.ForeignKey(
        "documents.Document",
        on_delete=models.CASCADE,
        related_name="access_entries",
        verbose_name=_(
            "Document",
        ),
        help_text=_(
            "Document being accessed.",
        ),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="document_access",
        verbose_name=_(
            "User",
        ),
        help_text=_(
            "User receiving access.",
        ),
    )

    # ============================================================
    # Permission
    # ============================================================

    permission = models.CharField(
        _("Permission"),
        max_length=30,
        choices=DocumentPermission.choices,
        default=DocumentPermission.VIEW,
        db_index=True,
    )

    # ============================================================
    # Lifecycle
    # ============================================================

    is_active = models.BooleanField(
        _("Active"),
        default=True,
        db_index=True,
        help_text=_(
            "Whether access is currently active.",
        ),
    )

    expires_at = models.DateTimeField(
        _("Expires At"),
        null=True,
        blank=True,
        help_text=_(
            "Optional access expiration.",
        ),
    )

    # ============================================================
    # Metadata
    # ============================================================

    metadata = models.JSONField(
        _("Metadata"),
        default=dict,
        blank=True,
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "document_access"

        verbose_name = _(
            "Document Access",
        )

        verbose_name_plural = _(
            "Document Access Entries",
        )

        ordering = (
            "document",
            "user",
        )

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "document",
                    "user",
                    "permission",
                ),
                name=("uq_document_user_permission"),
            ),
        ]

        indexes = [
            models.Index(
                fields=("document",),
                name=("idx_document_access_document"),
            ),
            models.Index(
                fields=("user",),
                name=("idx_document_access_user"),
            ),
            models.Index(
                fields=("permission",),
                name=("idx_document_access_permission"),
            ),
            models.Index(
                fields=("is_active",),
                name=("idx_document_access_active"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Human readable representation.
        """

        return f"{self.document.title} - {self.user_id} - {self.permission}"


__all__ = ("DocumentAccess",)
