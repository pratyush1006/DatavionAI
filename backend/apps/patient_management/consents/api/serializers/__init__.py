"""
Patient Consent serializer exports.
"""

from __future__ import annotations

from .create import (
    PatientConsentCreateSerializer,
)
from .detail import (
    PatientConsentDetailSerializer,
)
from .list import (
    PatientConsentListSerializer,
)
from .update import (
    PatientConsentUpdateSerializer,
)

__all__ = (
    "PatientConsentCreateSerializer",
    "PatientConsentDetailSerializer",
    "PatientConsentListSerializer",
    "PatientConsentUpdateSerializer",
)
