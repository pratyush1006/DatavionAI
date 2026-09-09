"""Query managers for patient emergency records."""

from __future__ import annotations

from django.db import models


class EmergencyRecordQuerySet(models.QuerySet):
    """Provide reusable queryset helpers for emergency records."""

    def active(self):
        """Return records that are currently active."""

        return self.filter(is_deleted=False, status="active")


class EmergencyRecordManager(models.Manager):
    """Expose the default emergency record queryset."""

    def get_queryset(self):
        """Return the base queryset for emergency records."""

        return EmergencyRecordQuerySet(self.model, using=self._db).filter(
            is_deleted=False,
        )


__all__ = (
    "EmergencyRecordManager",
    "EmergencyRecordQuerySet",
)
