"""
Organization feature entitlement model.

Stores organization-level feature entitlements.

Feature definitions are managed by the DatavionOS
Feature Registry. This model stores only the
organization's entitlement state and configuration.

Future roadmap:
    Replace ``feature_code`` with a ForeignKey to the
    platform Feature Registry once the catalog module
    is introduced.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class OrganizationFeature(
    BaseModel,
):
    """
    Feature entitlement assigned to an organization.

    Relationship:

        Feature Registry
              │
              ▼
    OrganizationFeature
              │
              ▼
        Organization
              │
              ▼
            Tenant

    Notes:
        This model does not define platform features.
        It only stores organization-specific entitlement
        and configuration.
    """

    class FeatureStatus(
        models.TextChoices,
    ):
        """
        Organization feature entitlement status.
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
        related_name="feature_entitlements",
        db_index=True,
        verbose_name=_("Organization"),
        help_text=_(
            "Organization receiving this feature entitlement.",
        ),
    )

    # ------------------------------------------------------------------
    # Feature Registry Reference
    # ------------------------------------------------------------------

    feature_code = models.CharField(
        max_length=100,
        db_index=True,
        verbose_name=_("Feature Code"),
        help_text=_(
            "Unique feature identifier from the DatavionOS Feature Registry.",
        ),
    )

    # ------------------------------------------------------------------
    # Entitlement
    # ------------------------------------------------------------------

    status = models.CharField(
        max_length=20,
        choices=FeatureStatus.choices,
        default=FeatureStatus.ENABLED,
        db_index=True,
        verbose_name=_("Status"),
        help_text=_(
            "Current feature entitlement status.",
        ),
    )

    settings = models.JSONField(
        default=dict,
        blank=True,
        verbose_name=_("Settings"),
        help_text=_(
            "Organization-specific configuration for this feature.",
        ),
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    enabled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Enabled At"),
        help_text=_(
            "Timestamp when the feature was enabled.",
        ),
    )

    disabled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name=_("Disabled At"),
        help_text=_(
            "Timestamp when the feature was disabled.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organization_feature"

        verbose_name = _(
            "Organization Feature",
        )

        verbose_name_plural = _(
            "Organization Features",
        )

        ordering = ("feature_code",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "feature_code",
                ),
                name="uq_organization_feature",
            ),
        ]

        indexes = [
            models.Index(
                fields=(
                    "organization",
                    "status",
                ),
                name="idx_org_feature_status",
            ),
            models.Index(
                fields=("feature_code",),
                name="idx_feature_code",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the string representation.
        """

        return f"{self.organization} - {self.feature_code}"


__all__ = ("OrganizationFeature",)
