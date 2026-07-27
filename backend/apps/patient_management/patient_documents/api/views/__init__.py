"""
Patient Document API views.
"""

from .create import (
    PatientDocumentCreateAPIView,
)
from .delete import (
    PatientDocumentDeleteAPIView,
)
from .detail import (
    PatientDocumentDetailAPIView,
)
from .list import (
    PatientDocumentListAPIView,
)
from .update import (
    PatientDocumentUpdateAPIView,
)

__all__ = [
    "PatientDocumentCreateAPIView",
    "PatientDocumentDeleteAPIView",
    "PatientDocumentDetailAPIView",
    "PatientDocumentListAPIView",
    "PatientDocumentUpdateAPIView",
]
