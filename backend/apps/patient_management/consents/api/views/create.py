"""
Create API view for Patient Consents.
"""

from __future__ import annotations

from apps.common.api import BaseCreateAPIView
from apps.patient_management.consents.api.serializers import (
    ConsentCreateSerializer,
)
from apps.patient_management.consents.permissions import (
    ConsentPermission,
)


class ConsentCreateAPIView(BaseCreateAPIView):
    """
    Create a patient consent.
    """

    serializer_class = ConsentCreateSerializer
    permission_required = (ConsentPermission.CREATE,)
