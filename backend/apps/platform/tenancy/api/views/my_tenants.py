"""
User tenant API view.

Returns organizations available
for authenticated user.
"""

from __future__ import annotations

from rest_framework.permissions import (
    IsAuthenticated,
)

from apps.common.api.base_generics import (
    BaseGenericAPIView,
)
from apps.common.api.responses import (
    success_response,
)
from apps.platform.tenancy.api.serializers import (
    MyTenantSerializer,
)
from apps.platform.tenancy.selectors import (
    list_user_tenants,
)


class MyTenantListAPIView(
    BaseGenericAPIView,
):
    """
    List tenants available for current user.

    Used by:

    - Organization switcher
    - Dashboard bootstrap
    - Tenant selection
    """

    serializer_class = MyTenantSerializer

    permission_classes = (IsAuthenticated,)

    def get(
        self,
        request,
        *args,
        **kwargs,
    ):

        memberships = list_user_tenants(
            user_id=request.user.id,
        )

        serializer = self.get_serializer(
            memberships,
            many=True,
        )

        return success_response(
            request=request,
            data=serializer.data,
        )


__all__ = ("MyTenantListAPIView",)
