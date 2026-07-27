"""
Imaging study service.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from django.db import transaction

from apps.imaging.constants import StudyStatus
from apps.imaging.models import Study
from apps.platform.accounts.models import User


class StudyService:
    """
    Application service responsible for imaging study write operations.
    """

    @staticmethod
    @transaction.atomic
    def create(
        *,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Study:
        """
        Create a new imaging study.
        """

        study = Study(
            **validated_data,
        )

        study.full_clean()

        study.save()

        return study

    @staticmethod
    @transaction.atomic
    def update(
        *,
        instance: Study,
        validated_data: Mapping[str, Any],
        performed_by: User | None = None,
    ) -> Study:
        """
        Update an existing imaging study.
        """

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
    def delete(
        *,
        instance: Study,
        performed_by: User | None = None,
    ) -> Study:
        """
        Delete an imaging study.

        Note: For now this is a soft/active delete handled by the BaseModel
        is_active flag when the model supports it; otherwise it performs a
        hard delete.
        """

        # Prefer soft delete if the model has is_active
        if hasattr(instance, "is_active"):
            instance.is_active = False
            instance.full_clean()
            instance.save(update_fields=["is_active", "updated_at"])
            return instance

        instance.delete()
        return instance

    @staticmethod
    @transaction.atomic
    def cancel(
        *,
        instance: Study,
        performed_by: User | None = None,
    ) -> Study:
        """
        Cancel an imaging study.
        """

        instance.status = StudyStatus.CANCELLED

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
    def complete(
        *,
        instance: Study,
        performed_by: User | None = None,
    ) -> Study:
        """
        Mark an imaging study as completed.
        """

        instance.status = StudyStatus.COMPLETED

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
    def bulk_create(
        *,
        validated_data_list: list[Mapping[str, Any]],
        performed_by: User | None = None,
    ) -> list[Study]:
        """
        Create multiple imaging studies.
        """

        studies: list[Study] = []

        for validated_data in validated_data_list:
            study = Study(
                **validated_data,
            )

            study.full_clean()

            study.save()

            studies.append(study)

        return studies


__all__ = [
    "StudyService",
]
