"""
Serializers for Patient Relationships.
"""

from .create import (
    PatientRelationshipCreateSerializer,
)
from .detail import (
    PatientRelationshipDetailSerializer,
)
from .list import (
    PatientRelationshipListSerializer,
)
from .update import (
    PatientRelationshipUpdateSerializer,
)

__all__ = (
    "PatientRelationshipCreateSerializer",
    "PatientRelationshipDetailSerializer",
    "PatientRelationshipListSerializer",
    "PatientRelationshipUpdateSerializer",
)
