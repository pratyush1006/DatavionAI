"""
Serializers for the Patient Relationships module.
"""

from .create import RelationshipCreateSerializer
from .detail import RelationshipDetailSerializer
from .list import RelationshipListSerializer
from .update import RelationshipUpdateSerializer

__all__ = [
    "RelationshipCreateSerializer",
    "RelationshipDetailSerializer",
    "RelationshipListSerializer",
    "RelationshipUpdateSerializer",
]
