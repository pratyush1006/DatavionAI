"""
Permission mixins.

Reusable mixins for API views and viewsets.

These mixins are framework-level utilities and intentionally do not
contain any business-specific authorization logic.
"""

from __future__ import annotations

from typing import ClassVar

from rest_framework.permissions import BasePermission
from rest_framework.views import APIView


class PermissionRequiredMixin:
    """
    Mixin for views requiring a single permission class.
    """

    permission_classes: ClassVar[tuple[type[BasePermission], ...]] = ()

    @classmethod
    def get_permission_classes(
        cls,
    ) -> tuple[type[BasePermission], ...]:
        """
        Return the configured permission classes.
        """
        return cls.permission_classes


class MultiplePermissionsMixin:
    """
    Mixin for views requiring multiple permission classes.
    """

    permission_classes: ClassVar[tuple[type[BasePermission], ...]] = ()

    @classmethod
    def get_permission_classes(
        cls,
    ) -> tuple[type[BasePermission], ...]:
        """
        Return the configured permission classes.
        """
        return cls.permission_classes


class PermissionAPIView(
    PermissionRequiredMixin,
    APIView,
):
    """
    APIView with framework permission mixin.
    """

    permission_classes: ClassVar[tuple[type[BasePermission], ...]] = ()


__all__ = (
    "MultiplePermissionsMixin",
    "PermissionAPIView",
    "PermissionRequiredMixin",
)
