"""
Tenant list API view.
"""

from __future__ import annotations

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)
from apps.common.api.responses import (
    success_response,
)
from apps.platform.tenancy.api.serializers import (
    TenantListSerializer,
)
from apps.platform.tenancy.permissions import (
    IsPlatformAdmin,
)
from apps.platform.tenancy.selectors import (
    list_active_tenants,
)


class TenantListAPIView(
    BaseGenericAPIView,
):
    """
    List active tenants.

    Only platform administrators
    can view all tenants.
    """

    serializer_class = TenantListSerializer

    permission_classes = (IsPlatformAdmin,)

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):

        tenants = list_active_tenants()

        serializer = self.get_serializer(
            tenants,
            many=True,
        )

        return success_response(
            request=request,
            data=serializer.data,
        )


__all__ = ("TenantListAPIView",)
