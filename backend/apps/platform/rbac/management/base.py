"""
Base classes for RBAC seed management commands.
"""

from __future__ import annotations

from typing import Any

from django.core.management.base import BaseCommand
from django.db import models, transaction


class BaseSeedCommand(
    BaseCommand,
):
    """
    Base class for RBAC seed commands.

    Subclasses must define:

    - model
    - lookup_field
    - objects
    """

    model: type[models.Model] | None = None

    lookup_field = "code"

    objects: list[dict[str, Any]] | tuple[dict[str, Any], ...] = ()

    success_message = "Seed completed."

    def prepare_data(
        self,
        data: dict[str, Any],
    ) -> dict[str, Any]:
        """
        Prepare seed data before persisting.

        Subclasses may override this method to resolve
        foreign keys or transform values.
        """

        return data

    @transaction.atomic
    def handle(
        self,
        *args,
        **options,
    ) -> None:
        """
        Seed the configured model.
        """

        if self.model is None:
            raise ValueError(
                "model must be configured.",
            )

        created = 0
        updated = 0

        for item in self.objects:
            data = self.prepare_data(
                dict(item),
            )

            lookup_value = data[self.lookup_field]

            defaults = dict(data)

            defaults.pop(
                self.lookup_field,
            )

            _, was_created = self.model.objects.update_or_create(
                **{
                    self.lookup_field: lookup_value,
                },
                defaults=defaults,
            )

            if was_created:
                created += 1
            else:
                updated += 1

        self.stdout.write(
            self.style.SUCCESS(
                (f"{self.success_message} (created={created}, updated={updated})"),
            ),
        )


__all__ = [
    "BaseSeedCommand",
]
