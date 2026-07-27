"""
Patient Consent API views.
"""

from .create import ConsentCreateAPIView
from .delete import ConsentDeleteAPIView
from .detail import ConsentDetailAPIView
from .list import ConsentListAPIView
from .update import ConsentUpdateAPIView

__all__ = [
    "ConsentCreateAPIView",
    "ConsentDeleteAPIView",
    "ConsentDetailAPIView",
    "ConsentListAPIView",
    "ConsentUpdateAPIView",
]
