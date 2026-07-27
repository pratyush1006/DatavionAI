"""
Delete API view for Patient Consents.
"""

from __future__ import annotations

from apps.common.api import BaseDestroyAPIView
from apps.patient_management.consents.models import (
    Consent,
)
from apps.patient_management.consents.permissions import (
    ConsentPermission,
)


class ConsentDeleteAPIView(BaseDestroyAPIView):
    """
    Delete a patient consent.
    """

    queryset = Consent.objects.all()

    permission_required = (ConsentPermission.DELETE,)

    lookup_field = "id"
