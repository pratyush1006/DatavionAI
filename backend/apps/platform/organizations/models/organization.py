"""
Organization model.

Represents a tenant organization within the DatavionAI platform.
"""

from __future__ import annotations

from django.core.exceptions import ValidationError
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
    DEFAULT_SUBSCRIPTION_STATUS,
    DEFAULT_VERIFICATION_STATUS,
    ORGANIZATION_CATEGORY_TYPES,
    OrganizationCategory,
    OrganizationSize,
    OrganizationStatus,
    OrganizationType,
    SubscriptionStatus,
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
    Represents a tenant organization within DatavionAI.
    """

    objects = OrganizationManager()

    # -------------------------------------------------------------------------
    # Identity
    # -------------------------------------------------------------------------

    name = models.CharField(
        max_length=255,
        unique=True,
        help_text=_(
            "Legal organization name.",
        ),
    )

    display_name = models.CharField(
        max_length=255,
        blank=True,
        db_index=True,
        help_text=_(
            "Display name shown throughout the platform.",
        ),
    )

    code = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            validate_organization_code,
        ],
        help_text=_(
            "Unique organization code.",
        ),
    )

    slug = models.SlugField(
        max_length=100,
        unique=True,
        help_text=_(
            "Unique organization slug.",
        ),
    )

    # -------------------------------------------------------------------------
    # Classification
    # -------------------------------------------------------------------------

    category = models.CharField(
        max_length=50,
        choices=OrganizationCategory.choices,
        default=DEFAULT_ORGANIZATION_CATEGORY,
        db_index=True,
        help_text=_(
            "Organization category.",
        ),
    )

    organization_type = models.CharField(
        max_length=100,
        choices=OrganizationType.choices,
        default=DEFAULT_ORGANIZATION_TYPE,
        db_index=True,
        help_text=_(
            "Organization type.",
        ),
    )

    status = models.CharField(
        max_length=50,
        choices=OrganizationStatus.choices,
        default=DEFAULT_ORGANIZATION_STATUS,
        db_index=True,
        help_text=_(
            "Organization lifecycle status.",
        ),
    )

    size = models.CharField(
        max_length=30,
        choices=OrganizationSize.choices,
        default=DEFAULT_ORGANIZATION_SIZE,
        help_text=_(
            "Organization size.",
        ),
    )

    # -------------------------------------------------------------------------
    # Contact
    # -------------------------------------------------------------------------

    email = models.EmailField(
        blank=True,
        db_index=True,
        help_text=_(
            "Primary contact email.",
        ),
    )

    support_email = models.EmailField(
        blank=True,
        help_text=_(
            "Support contact email.",
        ),
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
        validators=[
            phone_number_validator,
        ],
        help_text=_(
            "Primary contact phone number.",
        ),
    )

    website = models.URLField(
        blank=True,
        max_length=500,
        help_text=_(
            "Official website.",
        ),
    )

    # -------------------------------------------------------------------------
    # Address
    # -------------------------------------------------------------------------

    address = models.TextField(
        blank=True,
        help_text=_(
            "Primary organization address.",
        ),
    )

    city = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text=_(
            "City.",
        ),
    )

    state = models.CharField(
        max_length=100,
        blank=True,
        db_index=True,
        help_text=_(
            "State or province.",
        ),
    )

    country = models.CharField(
        max_length=100,
        default="India",
        db_index=True,
        help_text=_(
            "Country.",
        ),
    )

    postal_code = models.CharField(
        max_length=20,
        blank=True,
        help_text=_(
            "Postal code.",
        ),
    )

    timezone = models.CharField(
        max_length=100,
        default="Asia/Kolkata",
        help_text=_(
            "Organization timezone.",
        ),
    )

    # -------------------------------------------------------------------------
    # Legal
    # -------------------------------------------------------------------------

    registration_number = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "Business registration number.",
        ),
    )

    tax_number = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "Tax or GST number.",
        ),
    )

    license_number = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "Healthcare license number.",
        ),
    )

    accreditation = models.CharField(
        max_length=100,
        blank=True,
        help_text=_(
            "Accreditation identifier (e.g. NABH/NABL).",
        ),
    )

    # -------------------------------------------------------------------------
    # SaaS Metadata
    # -------------------------------------------------------------------------

    verification_status = models.CharField(
        max_length=30,
        choices=VerificationStatus.choices,
        default=DEFAULT_VERIFICATION_STATUS,
        db_index=True,
        help_text=_(
            "Verification status.",
        ),
    )

    subscription_status = models.CharField(
        max_length=30,
        choices=SubscriptionStatus.choices,
        default=DEFAULT_SUBSCRIPTION_STATUS,
        db_index=True,
        help_text=_(
            "Subscription status.",
        ),
    )

    description = models.TextField(
        blank=True,
        help_text=_(
            "Organization description.",
        ),
    )

    is_verified = models.BooleanField(
        default=False,
        help_text=_(
            "Whether the organization has been verified.",
        ),
    )

    is_demo = models.BooleanField(
        default=False,
        help_text=_(
            "Whether this is a demo organization.",
        ),
    )

    # -------------------------------------------------------------------------
    # Validation
    # -------------------------------------------------------------------------

    def clean(
        self,
    ) -> None:
        """
        Validate the organization.
        """

        super().clean()

        valid_types = ORGANIZATION_CATEGORY_TYPES.get(
            self.category,
            set(),
        )

        if self.organization_type not in valid_types:
            raise ValidationError(
                {
                    "organization_type": _(
                        "Selected organization type is not valid "
                        "for the chosen category."
                    ),
                },
            )

    def save(
        self,
        *args,
        **kwargs,
    ) -> None:
        """
        Validate before saving.
        """

        if not self.display_name:
            self.display_name = self.name

        self.full_clean()

        super().save(
            *args,
            **kwargs,
        )

    class Meta:
        """
        Organization metadata.
        """

        db_table = "organizations"

        verbose_name = _("Organization")

        verbose_name_plural = _("Organizations")

        ordering = ("name",)

        indexes = [
            models.Index(
                fields=[
                    "is_active",
                ],
            ),
        ]

    def __str__(
        self,
    ) -> str:
        """
        Return the organization display name.
        """

        return self.display_name or self.name


__all__ = [
    "Organization",
]
