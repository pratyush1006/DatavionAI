"""
Organization module entitlement model.

Stores module access configuration
for organizations.

Module definitions and lifecycle are managed by:

    DatavionOS Module Registry

This model only manages:

    - organization access
    - entitlement status
    - tenant module settings
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class OrganizationModule(
    BaseModel,
):
    """
    Organization module entitlement.

    Architecture:

        DatavionOS Module Registry
                    |
                    |
        OrganizationModule
                    |
                    |
             Organization
                    |
                  Tenant
    """

    class Status(
        models.TextChoices,
    ):
        """
        Module entitlement states.
        """

        ENABLED = (
            "enabled",
            _("Enabled"),
        )

        DISABLED = (
            "disabled",
            _("Disabled"),
        )

        TRIAL = (
            "trial",
            _("Trial"),
        )

        LOCKED = (
            "locked",
            _("Locked"),
        )

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="module_entitlements",
        db_index=True,
        help_text=_(
            "Organization receiving this module entitlement.",
        ),
    )

    # ------------------------------------------------------------------
    # Module Registry Reference
    # ------------------------------------------------------------------

    module_code = models.CharField(
        max_length=100,
        db_index=True,
        help_text=_(
            "Module identifier from DatavionOS registry.",
        ),
    )

    # ------------------------------------------------------------------
    # Entitlement State
    # ------------------------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ENABLED,
        db_index=True,
        help_text=_(
            "Current module entitlement state.",
        ),
    )

    settings = models.JSONField(
        default=dict,
        blank=True,
        help_text=_(
            "Organization-specific module configuration.",
        ),
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    enabled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_(
            "Module activation timestamp.",
        ),
    )

    disabled_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_(
            "Module disable timestamp.",
        ),
    )

    class Meta:
        db_table = "organization_module"

        verbose_name = _(
            "Organization Module",
        )

        verbose_name_plural = _(
            "Organization Modules",
        )

        ordering = ("module_code",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "module_code",
                ],
                name=("uq_organization_module"),
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
                name=("idx_org_module_status"),
            ),
            models.Index(
                fields=[
                    "module_code",
                ],
                name=("idx_module_code"),
            ),
        ]

    def __str__(
        self,
    ) -> str:
        return f"{self.organization} - {self.module_code}"


__all__ = [
    "OrganizationModule",
]
