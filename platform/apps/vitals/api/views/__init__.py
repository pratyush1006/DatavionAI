"""
Vital API views.
"""

from .list_create import (
    VitalListCreateAPIView,
)
from .retrieve_update_destroy import (
    VitalRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "VitalListCreateAPIView",
    "VitalRetrieveUpdateDestroyAPIView",
]
