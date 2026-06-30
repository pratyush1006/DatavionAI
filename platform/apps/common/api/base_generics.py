"""
Shared DRF generic API views.

These classes provide common behavior through reusable mixins
while leaving business workflows inside feature applications.
"""

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

from apps.common.api.mixins import (
    PermissionMapMixin,
    SelectorMixin,
    SerializerMapMixin,
)


class BaseListCreateAPIView(
    PermissionMapMixin,
    SerializerMapMixin,
    SelectorMixin,
    ListCreateAPIView,
):
    """
    Base class for list/create API endpoints.

    Business logic should remain inside feature views and
    service layer implementations.
    """

    pass


class BaseRetrieveUpdateDestroyAPIView(
    PermissionMapMixin,
    SerializerMapMixin,
    SelectorMixin,
    RetrieveUpdateDestroyAPIView,
):
    """
    Base class for retrieve/update/delete API endpoints.

    Business logic should remain inside feature views and
    service layer implementations.
    """

    pass


__all__ = [
    "BaseListCreateAPIView",
    "BaseRetrieveUpdateDestroyAPIView",
]
