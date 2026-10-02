"""Patient-owned dashboard endpoint."""

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.patient_management.portal.api.serializers.dashboard import (
    PatientDashboardSerializer,
)
from apps.patient_management.portal.selectors.dashboard import (
    get_patient_portal_account_for_user,
)
from apps.patient_management.portal.services.dashboard import build_patient_dashboard


class PatientSelfDashboardAPIView(APIView):
    """Return the authenticated patient's own dashboard projection."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        account = get_patient_portal_account_for_user(user=request.user)
        if account is None:
            raise PermissionDenied(
                "No unique, active, verified patient portal account is linked to this login."
            )

        payload = build_patient_dashboard(account=account)
        return Response(PatientDashboardSerializer(payload).data)


__all__ = ("PatientSelfDashboardAPIView",)
