from django.conf import settings
from django.db import connection
from django.utils import timezone
from rest_framework import status
from rest_framework.views import APIView

from apps.common.api.responses import success_response


class HealthCheckAPIView(APIView):
    """
    Health check endpoint.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request):
        database_status = "ok"

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            database_status = "error"

        data = {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "timestamp": timezone.now(),
            "checks": {
                "database": database_status,
            },
        }

        return success_response(
            message="Application is healthy.",
            data=data,
            status_code=status.HTTP_200_OK,
        )
