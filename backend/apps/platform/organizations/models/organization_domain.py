"""
Organization domain model.

Handles custom domains and tenant routing
for white-label DatavionOS deployments.

Responsibilities:

- Domain ownership
- Domain purpose
- Verification lifecycle
- SSL metadata

Routing resolution is handled by:
    DatavionOS Bootstrap
"""

from __future__ import annotations

from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class OrganizationDomain(
    BaseModel,
):
    """
    Custom domain configuration for an organization.

    Example:

        hospital.datavion.ai
        app.examplehospital.com

    Relationship:

        Tenant
            |
        Organization
            |
        OrganizationDomain
    """

    class DomainType(
        models.TextChoices,
    ):
        """
        Domain purpose.
        """

        PRIMARY = (
            "primary",
            _("Primary"),
        )

        LOGIN = (
            "login",
            _("Login"),
        )

        API = (
            "api",
            _("API"),
        )

        EMAIL = (
            "email",
            _("Email"),
        )

    class VerificationStatus(
        models.TextChoices,
    ):
        """
        Domain verification lifecycle.
        """

        PENDING = (
            "pending",
            _("Pending"),
        )

        VERIFIED = (
            "verified",
            _("Verified"),
        )

        FAILED = (
            "failed",
            _("Failed"),
        )

    # ------------------------------------------------------------------
    # Organization
    # ------------------------------------------------------------------

    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="domains",
        db_index=True,
        help_text=_(
            "Organization owning this domain.",
        ),
    )

    # ------------------------------------------------------------------
    # Domain Identity
    # ------------------------------------------------------------------

    domain = models.CharField(
        max_length=255,
        unique=True,
        db_index=True,
        help_text=_(
            "Fully qualified domain name.",
        ),
    )

    domain_type = models.CharField(
        max_length=20,
        choices=DomainType.choices,
        default=DomainType.PRIMARY,
        db_index=True,
        help_text=_(
            "Purpose of this domain.",
        ),
    )

    is_primary = models.BooleanField(
        default=False,
        db_index=True,
        help_text=_(
            "Whether this is the primary organization domain.",
        ),
    )

    # ------------------------------------------------------------------
    # Verification
    # ------------------------------------------------------------------

    verification_status = models.CharField(
        max_length=20,
        choices=VerificationStatus.choices,
        default=VerificationStatus.PENDING,
        db_index=True,
        help_text=_(
            "Domain verification state.",
        ),
    )

    verification_token_hash = models.CharField(
        max_length=255,
        blank=True,
        help_text=_(
            "Hashed DNS verification token.",
        ),
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_(
            "Timestamp when domain was verified.",
        ),
    )

    # ------------------------------------------------------------------
    # SSL
    # ------------------------------------------------------------------

    ssl_enabled = models.BooleanField(
        default=False,
        help_text=_(
            "Whether SSL certificate is enabled.",
        ),
    )

    ssl_expiry_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text=_(
            "SSL certificate expiry date.",
        ),
    )

    # ------------------------------------------------------------------
    # Metadata
    # ------------------------------------------------------------------

    class Meta:
        db_table = "organization_domain"

        verbose_name = _(
            "Organization Domain",
        )

        verbose_name_plural = _(
            "Organization Domains",
        )

        ordering = ("domain",)

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                ],
                condition=Q(
                    is_primary=True,
                ),
                name=("uq_org_primary_domain"),
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "is_primary",
                ],
                name=("idx_org_primary_domain"),
            ),
            models.Index(
                fields=[
                    "verification_status",
                ],
                name=("idx_domain_verification"),
            ),
        ]

    # ------------------------------------------------------------------
    # Entity Behavior
    # ------------------------------------------------------------------

    def __str__(
        self,
    ) -> str:
        return self.domain


__all__ = [
    "OrganizationDomain",
]
