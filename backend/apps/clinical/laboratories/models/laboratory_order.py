"""
Laboratory order model.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.encounters.models import Encounter
from apps.clinical.laboratories.constants import (
    DEFAULT_LABORATORY_ORDER_STATUS,
    DEFAULT_LABORATORY_PRIORITY,
    LaboratoryOrderStatus,
    LaboratoryPriority,
)
from apps.clinical.patients.models import Patient
from apps.clinical.providers.models import Provider
from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.platform.organizations.models import Organization


class LaboratoryOrder(BaseModel):
    """
    Represents a laboratory order placed for a patient.
    """

    objects = BaseManager()

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name="laboratory_orders",
        help_text="Organization that owns this laboratory order.",
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="laboratory_orders",
        help_text="Patient associated with this laboratory order.",
    )

    provider = models.ForeignKey(
        Provider,
        on_delete=models.CASCADE,
        related_name="laboratory_orders",
        help_text="Provider who ordered the laboratory investigation.",
    )

    encounter = models.ForeignKey(
        Encounter,
        on_delete=models.CASCADE,
        related_name="laboratory_orders",
        help_text="Encounter during which the laboratory order was placed.",
    )

    order_number = models.CharField(
        max_length=30,
        db_index=True,
        help_text="Unique laboratory order number.",
    )

    priority = models.CharField(
        max_length=20,
        choices=LaboratoryPriority.choices,
        default=DEFAULT_LABORATORY_PRIORITY,
        db_index=True,
        help_text="Priority assigned to the laboratory order.",
    )

    status = models.CharField(
        max_length=30,
        choices=LaboratoryOrderStatus.choices,
        default=DEFAULT_LABORATORY_ORDER_STATUS,
        db_index=True,
        help_text="Current status of the laboratory order.",
    )

    ordered_at = models.DateTimeField(
        db_index=True,
        help_text="Date and time when the laboratory order was placed.",
    )

    clinical_notes = models.TextField(
        blank=True,
        help_text="Clinical information supporting the laboratory request.",
    )

    instructions = models.TextField(
        blank=True,
        help_text="Additional specimen collection or processing instructions.",
    )

    class Meta:
        """
        Model metadata.
        """

        db_table = "laboratory_orders"

        verbose_name = "Laboratory Order"

        verbose_name_plural = "Laboratory Orders"

        ordering = ("-ordered_at",)

        indexes = [
            models.Index(
                fields=[
                    "organization",
                ],
            ),
            models.Index(
                fields=[
                    "patient",
                ],
            ),
            models.Index(
                fields=[
                    "provider",
                ],
            ),
            models.Index(
                fields=[
                    "encounter",
                ],
            ),
            models.Index(
                fields=[
                    "order_number",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "ordered_at",
                ],
            ),
            models.Index(
                fields=[
                    "organization",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "patient",
                    "ordered_at",
                ],
            ),
            models.Index(
                fields=[
                    "encounter",
                    "ordered_at",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "organization",
                    "order_number",
                ),
                name="unique_laboratory_order_per_organization",
            ),
        ]

    @property
    def title(
        self,
    ) -> str:
        """
        Return a human-readable title.
        """

        return (
            f"{self.order_number} | "
            f"{self.patient.full_name} | "
            f"{self.ordered_at:%Y-%m-%d %H:%M}"
        )

    @property
    def is_active(
        self,
    ) -> bool:
        """
        Return whether the laboratory order is active.
        """

        return self.status not in {
            LaboratoryOrderStatus.COMPLETED,
            LaboratoryOrderStatus.CANCELLED,
        }

    @property
    def is_completed(
        self,
    ) -> bool:
        """
        Return whether the laboratory order is completed.
        """

        return self.status == LaboratoryOrderStatus.COMPLETED

    @property
    def is_cancelled(
        self,
    ) -> bool:
        """
        Return whether the laboratory order is cancelled.
        """

        return self.status == LaboratoryOrderStatus.CANCELLED

    def __str__(
        self,
    ) -> str:
        """
        Return the string representation.
        """

        return self.title


__all__ = [
    "LaboratoryOrder",
]
