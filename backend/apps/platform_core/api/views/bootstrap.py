"""
Platform bootstrap API.
"""

from __future__ import annotations

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.platform_core.api.serializers.bootstrap import (
    PlatformBootstrapSerializer,
)
from apps.platform_core.builders.bootstrap import (
    platform_bootstrap_builder,
)
from apps.platform_core.builders.dashboard import (
    DashboardBuilder,
)
from apps.platform_core.builders.navigation import (
    NavigationBuilder,
)
from apps.platform_core.registries.module_registry import (
    module_registry,
)
from apps.platform_core.resolvers.branding import (
    branding_resolver,
)
from apps.platform_core.resolvers.feature_flags import (
    feature_flag_resolver,
)
from apps.platform_core.selectors.bootstrap import (
    platform_bootstrap_selector,
)


@extend_schema(
    tags=["Platform"],
    responses=PlatformBootstrapSerializer,
)
class PlatformBootstrapAPIView(APIView):
    """
    Return the platform bootstrap payload.
    """

    permission_classes = [IsAuthenticated]

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        Return the platform bootstrap payload.
        """

        context = platform_bootstrap_selector.get(
            user=request.user,
        )

        modules = module_registry.all()

        feature_flags = feature_flag_resolver.resolve(
            user=request.user,
        )

        branding = branding_resolver.resolve(
            organization=context.organization,
        )

        navigation = NavigationBuilder().build(
            permissions=context.permissions,
        )

        dashboard = DashboardBuilder().build(
            modules=modules,
            permissions=context.permissions,
            feature_flags=feature_flags,
        )

        bootstrap = platform_bootstrap_builder.build(
            context=context,
            modules=modules,
            navigation=navigation,
            dashboard=dashboard,
            branding=branding,
            feature_flags=feature_flags,
        )

        serializer = PlatformBootstrapSerializer(
            bootstrap,
        )

        return Response(
            serializer.data,
        )
