"""
Platform bootstrap API.

Returns the DatavionOS runtime bootstrap payload.

This endpoint is the runtime contract between:

Frontend Applications
        |
        v
DatavionOS Kernel
        |
        +----------------+
        |                |
    Tenant Context   RBAC Context
        |                |
        +----------------+
                 |
                 v
        Module Availability
                 |
                 v
 Navigation + Dashboard + Features
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
from apps.datavionos.builders.bootstrap import (
    platform_bootstrap_builder,
)
from apps.datavionos.builders.dashboard import (
    DashboardBuilder,
)
from apps.datavionos.builders.navigation import (
    NavigationBuilder,
)
from apps.datavionos.resolvers.branding import (
    branding_resolver,
)
from apps.datavionos.resolvers.feature_flags import (
    feature_flag_resolver,
)
from apps.datavionos.selectors.bootstrap import (
    platform_bootstrap_selector,
)
from apps.datavionos.selectors.module_availability import (
    module_availability_selector,
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
        Resolve and return runtime bootstrap.
        """

        print(
            "REQUEST TENANT:",
            getattr(
                request,
                "tenant",
                None,
            ),
        )

        print(
            "REQUEST TENANT CONTEXT:",
            getattr(
                request,
                "tenant_context",
                None,
            ),
        )

        #
        # Resolve authenticated runtime context.
        #
        context = platform_bootstrap_selector.get(
            user=request.user,
        )

        print(
            "BOOTSTRAP CONTEXT TENANT:",
            context.tenant,
        )

        #
        # Resolve subscription enabled modules.
        #
        modules = module_availability_selector.get(
            tenant=context.tenant,
        )

        #
        # Resolve tenant subscription feature entitlements.
        #
        # Subscription is the source of truth.
        #
        feature_flags = feature_flag_resolver.resolve(
            user=request.user,
            tenant=context.tenant,
        )

        #
        # Resolve organization branding.
        #
        branding = branding_resolver.resolve(
            organization=context.organization,
        )

        #
        # Build runtime navigation.
        #
        navigation = NavigationBuilder().build(
            modules=modules,
            permissions=context.permissions,
            feature_flags=feature_flags,
        )

        #
        # Build runtime dashboard.
        #
        dashboard = DashboardBuilder().build(
            modules=modules,
            permissions=context.permissions,
            feature_flags=feature_flags,
        )

        #
        # Resolve subscription metadata.
        #
        subscription = self._get_subscription(
            context=context,
        )

        #
        # Build immutable bootstrap contract.
        #
        bootstrap = platform_bootstrap_builder.build(
            context=context,
            modules=modules,
            navigation=navigation,
            dashboard=dashboard,
            branding=branding,
            feature_flags=feature_flags,
            subscription=subscription,
        )

        serializer = PlatformBootstrapSerializer(
            bootstrap,
        )

        return Response(
            serializer.data,
        )

    def _get_subscription(
        self,
        *,
        context,
    ) -> dict[str, object]:
        """
        Resolve tenant subscription metadata.
        """

        if context.tenant is None:
            return {}

        subscription = getattr(
            context.tenant,
            "subscription",
            None,
        )

        if subscription is None:
            return {}

        plan = subscription.plan

        return {
            "status": subscription.status,
            "auto_renew": subscription.auto_renew,
            "plan": {
                "name": plan.name,
                "code": plan.code,
                "billing_cycle": plan.billing_cycle,
            },
        }


__all__ = [
    "PlatformBootstrapAPIView",
]
