"""
Document API views.
"""

from .list_create import (
    DocumentListCreateAPIView,
)
from .retrieve_update_destroy import (
    DocumentRetrieveUpdateDestroyAPIView,
)

__all__ = (
    "DocumentListCreateAPIView",
    "DocumentRetrieveUpdateDestroyAPIView",
)
