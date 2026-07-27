"""
Shared building blocks for the Revenue Cycle Management application.
"""

from __future__ import annotations

from typing import Any

from django.db import transaction


class RcmService:
    """
    Generic write-side service for RCM entities.

    Subclasses set ``model`` to gain create / update / delete behaviour
    with validation.
    """

    model: type[Any]

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
    "RcmService",
]
