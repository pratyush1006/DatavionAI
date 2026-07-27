"""
Patient Document serializers.
"""

from .create import (
    PatientDocumentCreateSerializer,
)
from .detail import (
    PatientDocumentDetailSerializer,
)
from .list import (
    PatientDocumentListSerializer,
)
from .update import (
    PatientDocumentUpdateSerializer,
)

__all__ = [
    "PatientDocumentCreateSerializer",
    "PatientDocumentDetailSerializer",
    "PatientDocumentListSerializer",
    "PatientDocumentUpdateSerializer",
]
