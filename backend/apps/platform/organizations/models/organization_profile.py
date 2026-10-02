"""
Organization profile model.

Defines organization identity and classification
for DatavionOS dynamic tenant configuration.
"""

from __future__ import annotations

from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import BaseModel


class OrganizationProfile(BaseModel):
    """
    Extended profile information for an organization.

    Controls tenant classification and
    future module provisioning.
    """

    class Industry(models.TextChoices):
        """Organization industry."""

        HEALTHCARE = "healthcare", _("Healthcare")
        FINTECH = "fintech", _("FinTech")
        EDUCATION = "education", _("Education")
        OTHER = "other", _("Other")

    class FacilityType(models.TextChoices):
        """Healthcare facility types."""

        CLINIC = "clinic", _("Clinic")
        HOSPITAL = "hospital", _("Hospital")
        LABORATORY = "laboratory", _("Laboratory")
        PHARMACY = "pharmacy", _("Pharmacy")
        DIAGNOSTIC_CENTER = (
            "diagnostic_center",
            _("Diagnostic Center"),
        )
        INSURANCE = "insurance", _("Insurance Provider")
        CORPORATE = (
            "corporate",
            _("Corporate Healthcare"),
        )
        OTHER = "other", _("Other")

    organization = models.OneToOneField(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="profile",
        verbose_name=_("Organization"),
        help_text=_("Organization profile."),
    )

    industry = models.CharField(
        _("Industry"),
        max_length=50,
        choices=Industry.choices,
        default=Industry.HEALTHCARE,
        db_index=True,
        help_text=_("Industry category."),
    )

    facility_type = models.CharField(
        _("Facility Type"),
        max_length=50,
        choices=FacilityType.choices,
        default=FacilityType.CLINIC,
        db_index=True,
        help_text=_("Healthcare facility type."),
    )

    description = models.TextField(
        _("Description"),
        blank=True,
        help_text=_("Organization description."),
    )

    established_year = models.PositiveIntegerField(
        _("Established Year"),
        null=True,
        blank=True,
        help_text=_("Year the organization was established."),
    )

    employee_count = models.PositiveIntegerField(
        _("Employee Count"),
        default=0,
        help_text=_("Number of employees."),
    )

    bed_capacity = models.PositiveIntegerField(
        _("Bed Capacity"),
        default=0,
        help_text=_("Hospital bed capacity."),
    )

    license_number = models.CharField(
        _("License Number"),
        max_length=255,
        blank=True,
        help_text=_("Primary healthcare license number."),
    )

    metadata = models.JSONField(
        _("Metadata"),
        default=dict,
        blank=True,
        help_text=_("Additional organization metadata."),
    )

    class Meta:
        db_table = "organization_profile"
        verbose_name = _("Organization Profile")
        verbose_name_plural = _("Organization Profiles")

        indexes = [
            models.Index(
                fields=["industry"],
                name="idx_org_profile_industry",
            ),
            models.Index(
                fields=["facility_type"],
                name="idx_org_profile_facility",
            ),
        ]

    def clean(self) -> None:
        """
        Perform model-level validation.
        """
        super().clean()

        if self.established_year and self.established_year > date.today().year:
            raise ValidationError(
                {
                    "established_year": _("Established year cannot be in the future."),
                }
            )

    def __str__(self) -> str:
        """Return the organization name."""

        return str(self.organization)


__all__: tuple[str, ...] = ("OrganizationProfile",)
