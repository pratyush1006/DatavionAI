"""
Reusable QuerySet classes.
"""

from django.db import models


class BaseQuerySet(models.QuerySet):
    """
    Base queryset shared across business models.
    """

    def active(self):
        return self.filter(is_active=True)

    def inactive(self):
        return self.filter(is_active=False)

    def ordered(self):
        return self.order_by("-created_at")
