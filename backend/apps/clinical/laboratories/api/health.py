from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.clinical.permissions import ClinicalAPIPermission

from ..services.health import laboratory_health


class LaboratoryHealthAPIView(APIView):
    permission_classes = (IsAuthenticated, ClinicalAPIPermission)

    def get(self, request):
        return Response(laboratory_health())
