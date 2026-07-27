"""
List API view for Patient Consents.
"""

from __future__ import annotations

from apps.common.api import BaseListAPIView
from apps.patient_management.consents.api.filters import (
    ConsentFilter,
)
from apps.patient_management.consents.api.serializers import (
    ConsentListSerializer,
)
from apps.patient_management.consents.models import (
    Consent,
)
from apps.patient_management.consents.permissions import (
    ConsentPermission,
)


class ConsentListAPIView(BaseListAPIView):
    """
    List patient consents.
    """

    queryset = Consent.objects.select_related(
        "organization",
        "patient",
        "doctor",
        "guardian",
    )

    serializer_class = ConsentListSerializer

    filterset_class = ConsentFilter

    permission_required = (ConsentPermission.LIST,)
