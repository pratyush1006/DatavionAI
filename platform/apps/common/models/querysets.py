"""
Reusable QuerySet classes.
"""

from __future__ import annotations

from django.db import models


class BaseQuerySet(models.QuerySet):
    """
    Base queryset shared across business models.
    """

    def active(self):
        """
        Return only active records.
        """
        return self.filter(is_active=True)

    def inactive(self):
        """
        Return only inactive records.
        """
        return self.filter(is_active=False)
