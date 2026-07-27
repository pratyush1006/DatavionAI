"""
Health check API views.
"""

from __future__ import annotations

from datetime import UTC, datetime

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
    NOT_READY,
    READY,
)
from apps.core.health.checks import (
    application_health_checks,
)


def _timestamp() -> str:
    """
    Return the current UTC timestamp in ISO-8601 format.
    """

    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


class BaseHealthAPIView(APIView):
    """
    Base class for infrastructure health endpoints.

    These endpoints are intended for infrastructure monitoring
    and therefore:

    - Require no authentication
    - Are never throttled
    - Support GET requests only
    """

    permission_classes = (AllowAny,)
    authentication_classes: tuple = ()
    throttle_classes: tuple = ()
    http_method_names = ["get"]

    @staticmethod
    def _response(
        data: dict,
        *,
        status_code: int,
    ) -> Response:
        """
        Create a standardized health response.
        """

        response = Response(
            data,
            status=status_code,
        )

        response["Cache-Control"] = "no-store"
        response["Pragma"] = "no-cache"

        return response


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

        health = application_health_checks()

        return self._response(
            {
                "application": APP_NAME,
                "version": APP_VERSION,
                "timestamp": _timestamp(),
                **health,
            },
            status_code=(
                status.HTTP_200_OK
                if health["healthy"]
                else status.HTTP_503_SERVICE_UNAVAILABLE
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

        return self._response(
            {
                "application": APP_NAME,
                "version": APP_VERSION,
                "timestamp": _timestamp(),
                "status": ALIVE,
            },
            status_code=status.HTTP_200_OK,
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

        health = application_health_checks()

        return self._response(
            {
                "application": APP_NAME,
                "version": APP_VERSION,
                "timestamp": _timestamp(),
                "status": READY if health["healthy"] else NOT_READY,
                "checks": health["checks"],
            },
            status_code=(
                status.HTTP_200_OK
                if health["healthy"]
                else status.HTTP_503_SERVICE_UNAVAILABLE
            ),
        )


__all__ = [
    "BaseHealthAPIView",
    "HealthAPIView",
    "LivenessAPIView",
    "ReadinessAPIView",
]
