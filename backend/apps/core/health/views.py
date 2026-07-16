"""
Health check API views.
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.openapi import extend_schema
from apps.core.constants import (
    ALIVE,
    APP_NAME,
    APP_VERSION,
    HEALTHY,
    NOT_READY,
    READY,
    UNHEALTHY,
)
from apps.core.health.checks import (
    application_health_checks,
    is_application_ready,
)


class BaseHealthAPIView(APIView):
    """
    Base class for health endpoints.
    """

    permission_classes = (AllowAny,)

    authentication_classes: tuple = ()


class HealthAPIView(BaseHealthAPIView):
    """
    Return the overall application health status.
    """

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

        healthy = is_application_ready()

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


class LivenessAPIView(BaseHealthAPIView):
    """
    Kubernetes/Docker liveness probe.
    """

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


class ReadinessAPIView(BaseHealthAPIView):
    """
    Kubernetes/Docker readiness probe.
    """

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

        ready = is_application_ready()

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


__all__ = [
    "BaseHealthAPIView",
    "HealthAPIView",
    "LivenessAPIView",
    "ReadinessAPIView",
]
