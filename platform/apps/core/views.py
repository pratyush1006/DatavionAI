"""
Core application views.
"""

from __future__ import annotations

import logging

from django.conf import settings
from django.db import connection
from django.utils import timezone
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

logger = logging.getLogger("application")


class HealthCheckAPIView(APIView):
    """
    Health check endpoint.
    """

    authentication_classes = []
    permission_classes = []

    def get(
        self,
        request: Request,
    ) -> Response:
        database_status = "ok"

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
        except Exception:
            logger.exception(
                "Database health check failed.",
            )
            database_status = "error"

        data = {
            "status": "healthy",
            "version": settings.APP_VERSION,
            "timestamp": timezone.now(),
            "checks": {
                "database": database_status,
            },
        }

        return Response(
            data={
                "status": "success",
                "message": "Application is healthy.",
                "data": data,
            },
            status=status.HTTP_200_OK,
        )
