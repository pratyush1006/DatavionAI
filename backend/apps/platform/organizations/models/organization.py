"""
Organization model.

Represents a business organization inside
a DatavionOS SaaS tenant boundary.
"""

from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.common.validators import (
    phone_number_validator,
)
from apps.core.models import (
    BaseModel,
)
from apps.platform.organizations.constants import (
    DEFAULT_ORGANIZATION_CATEGORY,
    DEFAULT_ORGANIZATION_SIZE,
    DEFAULT_ORGANIZATION_STATUS,
    DEFAULT_ORGANIZATION_TYPE,
    DEFAULT_VERIFICATION_STATUS,
    OrganizationCategory,
    OrganizationSize,
    OrganizationStatus,
    OrganizationType,
    VerificationStatus,
)
from apps.platform.organizations.managers import (
    OrganizationManager,
)
from apps.platform.organizations.validators.organization import (
    validate_organization_code,
)


class Organization(
    BaseModel,
):
    """
    Business organization.

    SaaS hierarchy::

        Tenant
            └── Organization
                    ├── Profile
                    ├── Branding
                    ├── Domain
                    ├── Settings
                    ├── Feature Entitlements
                    └── Departments / Teams / Business Units

    Tenant isolation is managed by the
    Tenancy bounded context.
    """

    objects = OrganizationManager()

    # ------------------------------------------------------------------
    # Tenant Boundary
    # ------------------------------------------------------------------

    tenant = models.ForeignKey(
        "tenancy.Tenant",
        on_delete=models.CASCADE,
        related_name="organizations",
        db_index=True,
        verbose_name=_("Tenant"),
        help_text=_(
            "Tenant that owns this organization.",
        ),
    )

    # ------------------------------------------------------------------
    # Identity
    # ------------------------------------------------------------------

    name = models.CharField(
        _("Legal Name"),
        max_length=255,
        help_text=_(
            "Legal registered organization name.",
        ),
    )

    display_name = models.CharField(
        _("Display Name"),
        max_length=255,
        blank=True,
        db_index=True,
        help_text=_(
            "Friendly name displayed throughout the platform.",
        ),
    )

    code = models.CharField(
        _("Organization Code"),
        max_length=20,
        validators=[
            validate_organization_code,
        ],
        help_text=_(
            "Unique organization code within the tenant.",
        ),
    )

    slug = models.SlugField(
        _("Slug"),
        max_length=100,
        blank=True,
        help_text=_(
            "URL-friendly unique slug within the tenant.",
        ),
    )

    # ------------------------------------------------------------------
    # Classification
    # ------------------------------------------------------------------

    category = models.CharField(
        _("Category"),
        max_length=50,
        choices=OrganizationCategory.choices,
        default=DEFAULT_ORGANIZATION_CATEGORY,
        db_index=True,
    )

    organization_type = models.CharField(
        _("Organization Type"),
        max_length=100,
        choices=OrganizationType.choices,
        default=DEFAULT_ORGANIZATION_TYPE,
        db_index=True,
    )

    size = models.CharField(
        _("Organization Size"),
        max_length=30,
        choices=OrganizationSize.choices,
        default=DEFAULT_ORGANIZATION_SIZE,
    )

    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=OrganizationStatus.choices,
        default=DEFAULT_ORGANIZATION_STATUS,
        db_index=True,
    )

    # ------------------------------------------------------------------
    # Contact
    # ------------------------------------------------------------------

    email = models.EmailField(
        _("Email"),
        blank=True,
        db_index=True,
    )

    support_email = models.EmailField(
        _("Support Email"),
        blank=True,
    )

    phone = models.CharField(
        _("Phone"),
        max_length=20,
        blank=True,
        validators=[
            phone_number_validator,
        ],
    )

    website = models.URLField(
        _("Website"),
        blank=True,
        max_length=500,
    )

    # ------------------------------------------------------------------
    # Address
    # ------------------------------------------------------------------

    address = models.TextField(
        _("Address"),
        blank=True,
    )

    city = models.CharField(
        _("City"),
        max_length=100,
        blank=True,
        db_index=True,
    )

    state = models.CharField(
        _("State"),
        max_length=100,
        blank=True,
        db_index=True,
    )

    country = models.CharField(
        _("Country"),
        max_length=100,
        default="India",
        db_index=True,
    )

    postal_code = models.CharField(
        _("Postal Code"),
        max_length=20,
        blank=True,
    )

    timezone = models.CharField(
        _("Timezone"),
        max_length=100,
        default="Asia/Kolkata",
    )

    # ------------------------------------------------------------------
    # Legal Information
    # ------------------------------------------------------------------

    registration_number = models.CharField(
        _("Registration Number"),
        max_length=100,
        blank=True,
    )

    tax_number = models.CharField(
        _("Tax Number"),
        max_length=100,
        blank=True,
    )

    license_number = models.CharField(
        _("License Number"),
        max_length=100,
        blank=True,
    )

    accreditation = models.CharField(
        _("Accreditation"),
        max_length=100,
        blank=True,
    )

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    verification_status = models.CharField(
        _("Verification Status"),
        max_length=30,
        choices=VerificationStatus.choices,
        default=DEFAULT_VERIFICATION_STATUS,
        db_index=True,
    )

    description = models.TextField(
        _("Description"),
        blank=True,
    )

    is_demo = models.BooleanField(
        _("Demo Organization"),
        default=False,
        help_text=_(
            "Indicates whether this is a demo organization.",
        ),
    )

    class Meta:
        """
        Database metadata.
        """

        db_table = "organizations"

        verbose_name = _(
            "Organization",
        )

        verbose_name_plural = _(
            "Organizations",
        )

        ordering = ("name",)

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "tenant",
                    "name",
                ),
                name="uq_org_tenant_name",
            ),
            models.UniqueConstraint(
                fields=(
                    "tenant",
                    "code",
                ),
                name="uq_org_tenant_code",
            ),
            models.UniqueConstraint(
                fields=(
                    "tenant",
                    "slug",
                ),
                name="uq_org_tenant_slug",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "tenant",
                ],
                name="idx_org_tenant",
            ),
            models.Index(
                fields=[
                    "tenant",
                    "status",
                ],
                name="idx_org_tenant_status",
            ),
            models.Index(
                fields=[
                    "tenant",
                    "organization_type",
                ],
                name="idx_org_tenant_type",
            ),
            models.Index(
                fields=[
                    "category",
                ],
                name="idx_org_category",
            ),
            models.Index(
                fields=[
                    "country",
                ],
                name="idx_org_country",
            ),
            models.Index(
                fields=[
                    "verification_status",
                ],
                name="idx_org_verification",
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the human-readable organization name.
        """

        return self.display_name or self.name


__all__ = ("Organization",)
