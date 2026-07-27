"""
Patient Consent serializers.
"""

from .create import ConsentCreateSerializer
from .detail import ConsentDetailSerializer
from .list import ConsentListSerializer
from .update import ConsentUpdateSerializer

__all__ = [
    "ConsentCreateSerializer",
    "ConsentDetailSerializer",
    "ConsentListSerializer",
    "ConsentUpdateSerializer",
]
