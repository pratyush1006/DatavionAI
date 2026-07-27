"""
Retrieve API view for Patient Consents.
"""

from __future__ import annotations

from apps.common.api import BaseRetrieveAPIView
from apps.patient_management.consents.api.serializers import (
    ConsentDetailSerializer,
)
from apps.patient_management.consents.models import (
    Consent,
)
from apps.patient_management.consents.permissions import (
    ConsentPermission,
)


class ConsentDetailAPIView(BaseRetrieveAPIView):
    """
    Retrieve a patient consent.
    """

    queryset = Consent.objects.select_related(
        "organization",
        "patient",
        "doctor",
        "guardian",
    )

    serializer_class = ConsentDetailSerializer

    permission_required = (ConsentPermission.VIEW,)

    lookup_field = "id"
