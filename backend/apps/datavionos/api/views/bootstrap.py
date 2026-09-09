"""
DatavionOS platform bootstrap API.

Returns the authenticated user's tenant-aware DatavionOS runtime
bootstrap payload using the canonical DatavionOS API response envelope.

Runtime flow:

    Frontend
        |
        v
    PlatformBootstrapAPIView
        |
        v
    PlatformBootstrapSelector
        |
        +--> Tenant
        +--> Organization
        +--> Employee
        +--> RBAC
        +--> Effective Permissions
        |
        v
    PlatformBootstrapService
        |
        +--> SaaS Capabilities
        +--> Tenant Module Availability
        +--> Navigation
        +--> Dashboard
        |
        v
    PlatformBootstrapBuilder
        |
        v
    PlatformBootstrapSerializer
        |
        v
    success_response()
        |
        v
    JSON API Envelope
"""

from __future__ import annotations

from typing import Any

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import success_response
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
    Return the authenticated user's DatavionOS runtime bootstrap.

    The API view is intentionally thin.

    Responsibilities
    ----------------
    1. Resolve the authenticated runtime context.
    2. Pass the resolved context into the bootstrap service.
    3. Build the immutable bootstrap contract.
    4. Serialize the bootstrap payload.
    5. Wrap the payload in the canonical DatavionOS API envelope.

    Business rules remain inside selectors, resolvers, services,
    and builders.
    """

    permission_classes = [
        IsAuthenticated,
    ]

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Resolve and return the runtime bootstrap payload.
        """

        # ==============================================================
        # Runtime Context
        # ==============================================================

        context = platform_bootstrap_selector.get(
            user=request.user,
        )

        # ==============================================================
        # Bootstrap Service
        # ==============================================================

        result = PlatformBootstrapService().bootstrap(
            tenant=context.tenant,
            organization=context.organization,
            permissions=set(
                context.permissions,
            ),
        )

        # ==============================================================
        # Capabilities
        # ==============================================================

        capabilities = result.capabilities if result.capabilities is not None else {}

        # ==============================================================
        # Subscription
        # ==============================================================

        subscription = self._resolve_subscription(
            capabilities,
        )

        # ==============================================================
        # Bootstrap Contract
        # ==============================================================

        bootstrap = platform_bootstrap_builder.build(
            context=context,
            modules=(result.modules if result.modules is not None else []),
            navigation=(result.navigation if result.navigation is not None else []),
            dashboard=(result.dashboard if result.dashboard is not None else []),
            branding=(result.branding if result.branding is not None else {}),
            feature_flags=(
                result.feature_flags if result.feature_flags is not None else {}
            ),
            subscription=subscription,
            preferences=None,
        )

        # ==============================================================
        # Serialization
        # ==============================================================

        serializer = PlatformBootstrapSerializer(
            bootstrap,
        )

        # ==============================================================
        # Canonical DatavionOS API Envelope
        # ==============================================================

        return success_response(
            data=serializer.data,
            request=request,
        )

    # ==================================================================
    # Subscription
    # ==================================================================

    @staticmethod
    def _resolve_subscription(
        capabilities: dict[str, Any],
    ) -> dict[str, Any] | None:
        """
        Extract the subscription payload from runtime capabilities.

        EntitlementResolver returns a capability structure containing
        subscription metadata under:

            capabilities["capabilities"]["subscription"]

        The bootstrap serializer expects only the subscription object.
        """

        runtime_capabilities = capabilities.get(
            "capabilities",
        )

        if not isinstance(
            runtime_capabilities,
            dict,
        ):
            return None

        subscription = runtime_capabilities.get(
            "subscription",
        )

        if not isinstance(
            subscription,
            dict,
        ):
            return None

        return subscription


__all__ = ("PlatformBootstrapAPIView",)
