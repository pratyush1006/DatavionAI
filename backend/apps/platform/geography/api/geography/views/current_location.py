"""
One-time current-location API endpoint.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.platform.geography.api.geography.serializers.current_location import (
    CurrentLocationResponseSerializer,
    CurrentLocationSerializer,
)
from apps.platform.geography.exceptions import (
    GeocodingProviderError,
    InvalidCoordinatesError,
)
from apps.platform.geography.permissions.geography import (
    GeographyCurrentLocationPermission,
)
from apps.platform.geography.services.current_location import CurrentLocationService


class CurrentLocationAPIView(APIView):
    """Resolve coordinates obtained once from the browser/device."""

    permission_classes = (GeographyCurrentLocationPermission,)

    def post(self, request, *args, **kwargs):
        serializer = CurrentLocationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            result = CurrentLocationService().resolve(
                latitude=serializer.validated_data["latitude"],
                longitude=serializer.validated_data["longitude"],
                accuracy_meters=serializer.validated_data.get("accuracy_meters"),
            )
        except InvalidCoordinatesError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)
        except GeocodingProviderError as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_502_BAD_GATEWAY)

        output = CurrentLocationResponseSerializer(result)
        return Response(output.data, status=status.HTTP_200_OK)
