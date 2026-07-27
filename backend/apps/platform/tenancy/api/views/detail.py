"""
Tenant detail API view.
"""

from __future__ import annotations

from uuid import UUID

from rest_framework.exceptions import NotFound

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)
from apps.common.api.responses import (
    success_response,
)
from apps.platform.tenancy.api.serializers import (
    TenantDetailSerializer,
)
from apps.platform.tenancy.permissions import (
    HasTenantAccess,
)
from apps.platform.tenancy.selectors import (
    get_tenant,
)


class TenantDetailAPIView(
    BaseGenericAPIView,
):
    """
    Retrieve tenant details.

    Access controlled by tenant membership.
    """

    serializer_class = TenantDetailSerializer

    permission_classes = (HasTenantAccess,)

    def get(
        self,
        request,
        tenant_id: UUID,
        *args,
        **kwargs,
    ):

        tenant = get_tenant(
            tenant_id,
        )

        if not tenant:
            raise NotFound(
                "Tenant not found.",
            )

        serializer = self.get_serializer(
            tenant,
        )

        return success_response(
            request=request,
            data=serializer.data,
        )


__all__ = ("TenantDetailAPIView",)
