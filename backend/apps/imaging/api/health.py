from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.imaging.services.health import imaging_health


class ImagingHealthAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        return Response(imaging_health())
