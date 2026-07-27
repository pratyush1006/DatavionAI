"""
Imaging report service.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.imaging.constants import ReportStatus
from apps.imaging.models import Report
from apps.platform.accounts.models import User


class ReportService:
    """
    Application service responsible for imaging report write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Report:
        """
        Create a new imaging report.
        """

        report = Report(
            **validated_data,
        )

        report.full_clean()

        report.save()

        return report

    @staticmethod
    @transaction.atomic
    def finalize(
        *,
        instance: Report,
        performed_by: User | None = None,
    ) -> Report:
        """
        Finalize an imaging report.
        """

        instance.status = ReportStatus.FINALIZED

        instance.full_clean()

        instance.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return instance

    @staticmethod
    @transaction.atomic
    def amend(
        *,
        instance: Report,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Report:
        """
        Amend an existing imaging report.
        """

        instance.status = ReportStatus.AMENDED

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Report,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Report:
        """
        Update an existing imaging report.
        """

        instance.status = ReportStatus.AMENDED

        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @staticmethod
    @transaction.atomic
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: User | None = None,
    ) -> list[Report]:
        """
        Create multiple imaging reports.
        """

        reports: list[Report] = []

        for validated_data in validated_data_list:
            report = Report(
                **validated_data,
            )

            report.full_clean()

            report.save()

            reports.append(report)

        return reports


__all__ = [
    "ReportService",
]
