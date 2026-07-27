"""
Update API view for Patient Consents.
"""

from __future__ import annotations

from apps.common.api import BaseUpdateAPIView
from apps.patient_management.consents.api.serializers import (
    ConsentUpdateSerializer,
)
from apps.patient_management.consents.models import (
    Consent,
)
from apps.patient_management.consents.permissions import (
    ConsentPermission,
)


class ConsentUpdateAPIView(BaseUpdateAPIView):
    """
    Update a patient consent.
    """

    queryset = Consent.objects.all()

    serializer_class = ConsentUpdateSerializer

    permission_required = (ConsentPermission.UPDATE,)

    lookup_field = "id"
