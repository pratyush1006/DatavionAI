"""
Laboratory test model.
"""

from __future__ import annotations

from django.db import models

from apps.core.models import (
    BaseManager,
    BaseModel,
)
from apps.laboratories.constants import (
    DEFAULT_LABORATORY_PRIORITY,
    DEFAULT_LABORATORY_TEST_STATUS,
    LaboratoryCategory,
    LaboratoryPriority,
    LaboratorySpecimenType,
    LaboratoryTestStatus,
)
from apps.laboratories.models.laboratory_order import LaboratoryOrder


class LaboratoryTest(BaseModel):
    """
    Represents an individual laboratory test requested as part
    of a laboratory order.
    """

    objects = BaseManager()

    laboratory_order = models.ForeignKey(
        LaboratoryOrder,
        on_delete=models.CASCADE,
        related_name="tests",
        help_text="Laboratory order containing this test.",
    )

    code = models.CharField(
        max_length=30,
        db_index=True,
        help_text="Standard laboratory test code.",
    )

    name = models.CharField(
        max_length=255,
        db_index=True,
        help_text="Laboratory test name.",
    )

    category = models.CharField(
        max_length=30,
        choices=LaboratoryCategory.choices,
        db_index=True,
        help_text="Clinical category of the laboratory test.",
    )

    specimen_type = models.CharField(
        max_length=30,
        choices=LaboratorySpecimenType.choices,
        help_text="Required specimen type.",
    )

    priority = models.CharField(
        max_length=20,
        choices=LaboratoryPriority.choices,
        default=DEFAULT_LABORATORY_PRIORITY,
        db_index=True,
        help_text="Execution priority of the laboratory test.",
    )

    display_order = models.PositiveSmallIntegerField(
        default=1,
        db_index=True,
        help_text="Display order within the laboratory order.",
    )

    status = models.CharField(
        max_length=20,
        choices=LaboratoryTestStatus.choices,
        default=DEFAULT_LABORATORY_TEST_STATUS,
        db_index=True,
        help_text="Current status of the laboratory test.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional notes for the laboratory test.",
    )

    class Meta:
        """
        Model metadata.
        """

        db_table = "laboratory_tests"

        verbose_name = "Laboratory Test"

        verbose_name_plural = "Laboratory Tests"

        ordering = (
            "display_order",
            "name",
        )

        indexes = [
            models.Index(
                fields=[
                    "laboratory_order",
                ],
            ),
            models.Index(
                fields=[
                    "code",
                ],
            ),
            models.Index(
                fields=[
                    "name",
                ],
            ),
            models.Index(
                fields=[
                    "category",
                ],
            ),
            models.Index(
                fields=[
                    "priority",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "category",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "laboratory_order",
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "laboratory_order",
                    "display_order",
                ],
            ),
        ]

        constraints = [
            models.UniqueConstraint(
                fields=(
                    "laboratory_order",
                    "code",
                ),
                name="unique_test_per_laboratory_order",
            ),
        ]

    @property
    def title(
        self,
    ) -> str:
        """
        Return a human-readable title.
        """

        return f"{self.laboratory_order.order_number} | {self.name}"

    @property
    def is_pending(
        self,
    ) -> bool:
        """
        Return whether the laboratory test is pending.
        """

        return self.status == LaboratoryTestStatus.PENDING

    @property
    def is_in_progress(
        self,
    ) -> bool:
        """
        Return whether the laboratory test is currently in progress.
        """

        return self.status == LaboratoryTestStatus.IN_PROGRESS

    @property
    def is_completed(
        self,
    ) -> bool:
        """
        Return whether the laboratory test is completed.
        """

        return self.status == LaboratoryTestStatus.COMPLETED

    @property
    def is_cancelled(
        self,
    ) -> bool:
        """
        Return whether the laboratory test is cancelled.
        """

        return self.status == LaboratoryTestStatus.CANCELLED

    def __str__(
        self,
    ) -> str:
        """
        Return the string representation.
        """

        return self.title


__all__ = [
    "LaboratoryTest",
]
