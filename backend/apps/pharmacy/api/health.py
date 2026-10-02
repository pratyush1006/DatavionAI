from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.pharmacy.services.health import pharmacy_health


class PharmacyHealthAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(pharmacy_health())
