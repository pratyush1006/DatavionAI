"""
Laboratory result model.
"""

from __future__ import annotations

from django.db import models

from apps.clinical.laboratories.constants import (
    DEFAULT_LABORATORY_RESULT_FLAG,
    DEFAULT_LABORATORY_RESULT_STATUS,
    LaboratoryResultFlag,
    LaboratoryResultStatus,
)
from apps.clinical.laboratories.models.laboratory_test import LaboratoryTest
from apps.clinical.providers.models import Provider
from apps.core.models import (
    BaseManager,
    BaseModel,
)


class LaboratoryResult(BaseModel):
    """
    Represents the result of an individual laboratory test.
    """

    objects = BaseManager()

    laboratory_test = models.OneToOneField(
        LaboratoryTest,
        on_delete=models.CASCADE,
        related_name="result",
        help_text="Laboratory test associated with this result.",
    )

    result_value_numeric = models.DecimalField(
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Numeric laboratory result value.",
    )

    result_value_text = models.CharField(
        max_length=255,
        blank=True,
        help_text="Text laboratory result value.",
    )

    unit = models.CharField(
        max_length=50,
        blank=True,
        help_text="Measurement unit.",
    )

    reference_range = models.CharField(
        max_length=100,
        blank=True,
        help_text="Reference range for the laboratory test.",
    )

    abnormal_flag = models.CharField(
        max_length=30,
        choices=LaboratoryResultFlag.choices,
        default=DEFAULT_LABORATORY_RESULT_FLAG,
        db_index=True,
        help_text="Abnormality flag for the laboratory result.",
    )

    status = models.CharField(
        max_length=30,
        choices=LaboratoryResultStatus.choices,
        default=DEFAULT_LABORATORY_RESULT_STATUS,
        db_index=True,
        help_text="Current status of the laboratory result.",
    )

    resulted_at = models.DateTimeField(
        db_index=True,
        help_text="Date and time the laboratory result was generated.",
    )

    verified_by = models.ForeignKey(
        Provider,
        on_delete=models.SET_NULL,
        related_name="verified_laboratory_results",
        null=True,
        blank=True,
        help_text="Provider who verified the laboratory result.",
    )

    verified_at = models.DateTimeField(
        null=True,
        blank=True,
        db_index=True,
        help_text="Date and time the laboratory result was verified.",
    )

    notes = models.TextField(
        blank=True,
        help_text="Additional laboratory notes.",
    )

    class Meta:
        """
        Model metadata.
        """

        db_table = "laboratory_results"

        verbose_name = "Laboratory Result"

        verbose_name_plural = "Laboratory Results"

        ordering = ("-resulted_at",)

        indexes = [
            models.Index(
                fields=[
                    "laboratory_test",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                ],
            ),
            models.Index(
                fields=[
                    "resulted_at",
                ],
            ),
            models.Index(
                fields=[
                    "verified_by",
                ],
            ),
            models.Index(
                fields=[
                    "verified_at",
                ],
            ),
            models.Index(
                fields=[
                    "status",
                    "resulted_at",
                ],
            ),
            models.Index(
                fields=[
                    "abnormal_flag",
                    "resulted_at",
                ],
            ),
        ]

        constraints = [
            models.CheckConstraint(
                condition=(
                    models.Q(
                        result_value_numeric__isnull=False,
                    )
                    | ~models.Q(
                        result_value_text="",
                    )
                ),
                name="laboratory_result_has_value",
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
            f"{self.laboratory_test.name}"
            f" | "
            f"{self.laboratory_test.laboratory_order.order_number}"
        )

    @property
    def is_recorded(
        self,
    ) -> bool:
        """
        Return whether the laboratory result has been recorded.
        """

        return self.status == LaboratoryResultStatus.RECORDED

    @property
    def is_verified(
        self,
    ) -> bool:
        """
        Return whether the laboratory result has been verified.
        """

        return self.status == LaboratoryResultStatus.VERIFIED

    @property
    def is_amended(
        self,
    ) -> bool:
        """
        Return whether the laboratory result has been amended.
        """

        return self.status == LaboratoryResultStatus.AMENDED

    @property
    def is_invalidated(
        self,
    ) -> bool:
        """
        Return whether the laboratory result has been invalidated.
        """

        return self.status == LaboratoryResultStatus.INVALIDATED

    @property
    def is_final(
        self,
    ) -> bool:
        """
        Return whether the laboratory result is final.
        """

        return self.status == LaboratoryResultStatus.FINAL

    @property
    def is_active(
        self,
    ) -> bool:
        """
        Return whether the laboratory result is still active.
        """

        return not (self.is_final or self.is_invalidated)

    def __str__(
        self,
    ) -> str:
        """
        Return the string representation.
        """

        return self.title


__all__ = [
    "LaboratoryResult",
]
