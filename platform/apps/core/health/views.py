"""
Health check API views.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.core.constants import (
    ALIVE,
    APP_NAME,
    APP_VERSION,
    HEALTHY,
    NOT_READY,
    READY,
    UNHEALTHY,
)
from apps.core.health.checks import application_health_checks


class HealthAPIView(APIView):
    """
    Return the overall application health status.
    """

    permission_classes = [AllowAny]
    authentication_classes: list = []

    @extend_schema(
        tags=["Health"],
        summary="Application Health",
        description="Returns the overall application health status.",
    )
    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Return application health information.
        """

        checks = application_health_checks()

        healthy = all(result["healthy"] for result in checks.values())

        return Response(
            {
                "application": APP_NAME,
                "version": APP_VERSION,
                "status": HEALTHY if healthy else UNHEALTHY,
                "checks": checks,
            },
            status=(
                status.HTTP_200_OK if healthy else status.HTTP_503_SERVICE_UNAVAILABLE
            ),
        )


class LivenessAPIView(APIView):
    """
    Kubernetes/Docker liveness probe.
    """

    permission_classes = [AllowAny]
    authentication_classes: list = []

    @extend_schema(
        tags=["Health"],
        summary="Liveness Probe",
        description="Returns whether the application process is alive.",
    )
    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Return liveness status.
        """

        return Response(
            {
                "status": ALIVE,
            },
            status=status.HTTP_200_OK,
        )


class ReadinessAPIView(APIView):
    """
    Kubernetes/Docker readiness probe.
    """

    permission_classes = [AllowAny]
    authentication_classes: list = []

    @extend_schema(
        tags=["Health"],
        summary="Readiness Probe",
        description="Returns whether the application is ready to serve traffic.",
    )
    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Return readiness status.
        """

        checks = application_health_checks()

        ready = all(result["healthy"] for result in checks.values())

        return Response(
            {
                "application": APP_NAME,
                "version": APP_VERSION,
                "status": READY if ready else NOT_READY,
                "checks": checks,
            },
            status=(
                status.HTTP_200_OK if ready else status.HTTP_503_SERVICE_UNAVAILABLE
            ),
        )
