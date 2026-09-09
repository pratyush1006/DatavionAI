"""
Patient Profile API views.
"""

from .profile import (
    ProfileListCreateAPIView,
    ProfileRetrieveUpdateDestroyAPIView,
)

__all__ = (
    "ProfileListCreateAPIView",
    "ProfileRetrieveUpdateDestroyAPIView",
)
