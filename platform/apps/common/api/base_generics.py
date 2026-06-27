"""
Shared DRF generic API views.

These classes currently extend Django REST Framework generic
views without overriding their behavior. They provide a
centralized extension point for future cross-cutting concerns,
such as:

- Audit logging
- Organization scoping
- Request metrics
- Standardized API responses
- Soft delete support
"""

from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
)


class BaseListCreateAPIView(ListCreateAPIView):
    """
    Base class for list/create API endpoints.
    """

    pass


class BaseRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Base class for retrieve/update/delete API endpoints.
    """

    pass
