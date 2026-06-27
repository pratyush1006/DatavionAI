"""
Reusable model managers.
"""

from django.db import models

from .querysets import BaseQuerySet


class BaseManager(models.Manager):
    """
    Base manager exposing common queryset methods.
    """

    def get_queryset(self):
        return BaseQuerySet(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()

    def inactive(self):
        return self.get_queryset().inactive()

    def ordered(self):
        return self.get_queryset().ordered()
