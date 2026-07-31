"""
Platform bootstrap API.

Returns the DatavionOS runtime bootstrap payload.

Runtime flow:

Frontend
    |
    v
Platform Bootstrap API
    |
    v
PlatformBootstrapSelector
    |
    v
PlatformBootstrapService
    |
    +── Entitlements
    +── Modules
    +── Navigation
    +── Dashboard
    |
    v
PlatformBootstrapBuilder
    |
    v
PlatformBootstrapSerializer
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.datavionos.api.serializers.bootstrap import (
    PlatformBootstrapSerializer,
)
from apps.datavionos.bootstrap.service import (
    PlatformBootstrapService,
)
from apps.datavionos.builders.bootstrap import (
    platform_bootstrap_builder,
)
from apps.datavionos.selectors.bootstrap import (
    platform_bootstrap_selector,
)


@extend_schema(
    tags=[
        "Platform",
    ],
    responses=PlatformBootstrapSerializer,
)
class PlatformBootstrapAPIView(
    APIView,
):
    """
    Return DatavionOS runtime bootstrap payload.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Resolve runtime bootstrap.
        """

        #
        # Resolve identity + RBAC context
        #
        context = platform_bootstrap_selector.get(
            user=request.user,
        )

        #
        # Resolve DatavionOS runtime
        #
        result = PlatformBootstrapService().bootstrap(
            tenant=context.tenant,
            organization=context.organization,
        )

        #
        # Build frontend contract
        #
        bootstrap = platform_bootstrap_builder.build(
            context=context,
            modules=(result.modules or []),
            navigation=(result.navigation or []),
            dashboard=(result.dashboard or []),
            branding=(result.branding or {}),
            feature_flags=(result.feature_flags or {}),
            subscription=(
                result.capabilities.get(
                    "capabilities",
                    {},
                )
                if result.capabilities
                else {}
            ),
            preferences=None,
        )

        serializer = PlatformBootstrapSerializer(
            bootstrap,
        )

        return Response(
            serializer.data,
        )


__all__ = [
    "PlatformBootstrapAPIView",
]
