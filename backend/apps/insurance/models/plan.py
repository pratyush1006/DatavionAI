"""
Insurance plan model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import BaseManager, BaseModel
from apps.insurance.constants import (
    DEFAULT_INSURANCE_TYPE,
    InsuranceType,
)
from apps.platform.organizations.models import Organization


class InsurancePlan(BaseModel):
    """
    Represents an insurance plan offered by an organization.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="insurance_plans",
        help_text="Organization that owns the insurance plan.",
    )

    name = models.CharField(
        max_length=200,
        help_text="Insurance plan name.",
    )

    plan_code = models.CharField(
        max_length=50,
        help_text="Unique plan code within the organization.",
    )

    insurance_type = models.CharField(
        max_length=20,
        choices=InsuranceType.choices,
        default=DEFAULT_INSURANCE_TYPE,
        help_text="Type of insurance plan.",
    )

    coverage_details = models.JSONField(
        default=dict,
        blank=True,
        help_text="Plan coverage configuration and benefits.",
    )

    is_active = models.BooleanField(
        default=True,
        help_text="Whether the insurance plan is currently active.",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Timestamp when the plan was created.",
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp when the plan was last updated.",
    )

    class Meta:
        db_table = "insurance_plans"

        verbose_name = "Insurance Plan"

        verbose_name_plural = "Insurance Plans"

        ordering = (
            "organization",
            "name",
        )

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "organization",
                    "plan_code",
                ],
                name="unique_plan_code_per_organization",
            ),
        ]

        indexes = [
            models.Index(
                fields=[
                    "organization",
                    "is_active",
                ],
                name="insurance_plan_org_active_idx",
            ),
            models.Index(
                fields=[
                    "insurance_type",
                ],
                name="insurance_plan_type_idx",
            ),
        ]

    def __str__(self) -> str:
        """
        Return the plan display name.
        """

        return f"{self.name} ({self.plan_code})"


__all__ = [
    "InsurancePlan",
]
