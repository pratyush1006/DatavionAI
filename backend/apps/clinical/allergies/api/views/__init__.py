"""
Allergy API views.
"""

from .list_create import (
    AllergyListCreateAPIView,
)
from .retrieve_update_destroy import (
    AllergyRetrieveUpdateDestroyAPIView,
)

__all__ = [
    "AllergyListCreateAPIView",
    "AllergyRetrieveUpdateDestroyAPIView",
]
