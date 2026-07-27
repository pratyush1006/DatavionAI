"""
Tenant creation API view.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)
from apps.common.api.responses import (
    created_response,
)
from apps.platform.tenancy.api.serializers import (
    TenantCreateSerializer,
    TenantDetailSerializer,
)
from apps.platform.tenancy.permissions import (
    IsPlatformAdmin,
)
from apps.platform.tenancy.services import (
    TenantService,
)


class TenantCreateAPIView(
    BaseGenericAPIView,
):
    """
    Create tenant endpoint.

    Only platform administrators
    can create new tenants.
    """

    serializer_class = TenantCreateSerializer

    permission_classes = (IsPlatformAdmin,)

    def post(
        self,
        request,
        *args,
        **kwargs,
    ):
        serializer = self.get_serializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        tenant = TenantService.create_tenant(
            **serializer.validated_data,
        )

        response_serializer = TenantDetailSerializer(
            tenant,
        )

        return created_response(
            request=request,
            data=response_serializer.data,
        )


__all__ = ("TenantCreateAPIView",)
