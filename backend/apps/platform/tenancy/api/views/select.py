"""
Tenant selection API view.

Allows authenticated users to select
their active organization.
"""

from __future__ import annotations

from rest_framework.exceptions import (
    NotFound,
    PermissionDenied,
)
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
    TenantSelectSerializer,
)
from apps.platform.tenancy.models import (
    UserTenantPreference,
)
from apps.platform.tenancy.selectors import (
    get_active_tenant,
    get_tenant_membership,
)


class TenantSelectAPIView(
    BaseGenericAPIView,
):
    """
    Select active tenant.

    Flow:

    User
      |
      v
    TenantMembership
      |
      v
    UserTenantPreference
      |
      v
    Active Tenant
    """

    serializer_class = TenantSelectSerializer

    permission_classes = (IsAuthenticated,)

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

        tenant_id = serializer.validated_data["tenant_id"]

        tenant = get_active_tenant(
            tenant_id,
        )

        if tenant is None:
            raise NotFound(
                "Tenant not found.",
            )

        membership = get_tenant_membership(
            tenant_id=tenant.id,
            user_id=request.user.id,
        )

        if membership is None:
            raise PermissionDenied(
                "You do not have access to this tenant.",
            )

        UserTenantPreference.objects.update_or_create(
            user=request.user,
            defaults={
                "tenant": tenant,
            },
        )

        data = {
            "tenant_id": str(
                tenant.id,
            ),
            "name": tenant.name,
            "tenant_type": tenant.tenant_type,
            "role": ("OWNER" if membership.is_owner else "MEMBER"),
        }

        return success_response(
            request=request,
            data=data,
        )


__all__ = ("TenantSelectAPIView",)
