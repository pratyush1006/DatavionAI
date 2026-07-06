"""
Prescription API views.
"""

from .list_create import (
    PrescriptionListCreateAPIView,
)
from .retrieve_update_destroy import (
    PrescriptionRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "PrescriptionListCreateAPIView",
    "PrescriptionRetrieveUpdateDestroyAPIView",
]
