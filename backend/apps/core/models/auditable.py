"""
Auditable model foundation for the DatavionOS platform.

Provides creator and last-modifier ownership metadata for
audit-sensitive domain entities.

Architecture
------------
AuditableModel extends BaseModel and adds only audit ownership:

    BaseModel
        ├── UUID identity
        ├── timestamps
        ├── soft deletion
        └── active lifecycle
    AuditableModel
        ├── created_by
        └── updated_by

The model remains abstract and domain-agnostic.

Business applications are responsible for supplying the actor
through their service/workflow layer. This model does not contain
HTTP, RBAC, workflow, or domain-specific behavior.
"""

from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from .base import BaseModel


class AuditableModel(
    BaseModel,
):
    """
    Abstract model providing audit ownership metadata.

    ``created_by`` identifies the user that originally created
    the record.

    ``updated_by`` identifies the user that most recently changed
    the record.

    Both fields are nullable because system/background operations,
    migrations, imports, and historical records may legitimately
    have no authenticated human actor.
    """

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="created_%(class)ss",
        verbose_name=_("Created By"),
        help_text=_(
            "User that created this record.",
        ),
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        editable=False,
        related_name="updated_%(class)ss",
        verbose_name=_("Updated By"),
        help_text=_(
            "User that most recently updated this record.",
        ),
    )

    class Meta:
        """
        Django model metadata.
        """

        abstract = True


__all__: tuple[str, ...] = ("AuditableModel",)
