"""
Base serializers used across the DatavionAI platform.
"""

from __future__ import annotations

from typing import Any

from rest_framework import serializers


class BaseModelSerializer(serializers.ModelSerializer):
    """
    Base model serializer for the DatavionAI platform.

    All application serializers should inherit from this class
    instead of DRF's ``ModelSerializer``.

    This class serves as the central extension point for
    platform-wide serializer behavior while intentionally
    remaining lightweight.
    """

    class Meta:
        """
        Base serializer metadata.

        Concrete serializers must override this class.
        """

        abstract = True

    @property
    def request(
        self,
    ) -> Any:
        """
        Return the current request, if available.
        """

        return self.context.get("request")

    @property
    def user(
        self,
    ) -> Any:
        """
        Return the authenticated user, if available.
        """

        request = self.request

        return getattr(
            request,
            "user",
            None,
        )

    @property
    def organization(
        self,
    ) -> Any:
        """
        Return the current organization, if available.

        Organization resolution remains generic here.
        Concrete tenant/organization behavior belongs to
        application modules.
        """

        request = self.request

        return getattr(
            request,
            "organization",
            None,
        )


__all__: tuple[str, ...] = ("BaseModelSerializer",)
