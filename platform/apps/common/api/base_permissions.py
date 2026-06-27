"""
Shared DRF permission classes.

These classes centralize authentication and authorization
logic across the platform and serve as extension points
for future permission requirements.
"""

from rest_framework.permissions import IsAuthenticated


class BasePermission(IsAuthenticated):
    """
    Base permission class for all authenticated APIs.
    """

    pass
