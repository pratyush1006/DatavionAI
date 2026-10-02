"""
Shared building blocks for the Patient Management application.

These helpers centralize the repetitive lifecycle logic (create, update,
delete) that every Patient Management module implements, while still
allowing each module to own its own service class.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction


class PatientMgmtService:
    """
    Generic write-side service for Patient Management entities.

    Subclasses set ``model`` to gain create / update / delete behaviour
    with validation. Audit logging can be layered on by individual
    modules when required.
    """

    model: type[Any]

    @staticmethod
    def _serialize(value: Any) -> Any:
        if hasattr(value, "pk"):
            return str(value.pk)

        if hasattr(value, "id"):
            return str(value.id)

        return value

    @classmethod
    @transaction.atomic
    def create(
        cls,
        *,
        validated_data: dict[str, Any],
        performed_by: Any = None,
    ) -> Any:
        instance = cls.model(
            **validated_data,
        )

        instance.full_clean()

        instance.save()

        return instance

    @classmethod
    @transaction.atomic
    def update(
        cls,
        *,
        instance: Any,
        validated_data: dict[str, Any],
        performed_by: Any = None,
    ) -> Any:
        for field, value in validated_data.items():
            setattr(
                instance,
                field,
                value,
            )

        instance.full_clean()

        instance.save()

        return instance

    @classmethod
    @transaction.atomic
    def delete(
        cls,
        *,
        instance: Any,
        performed_by: Any = None,
    ) -> None:
        instance.delete()


__all__ = [
    "PatientMgmtService",
]
