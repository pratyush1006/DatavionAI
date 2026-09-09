"""
DatavionOS platform bootstrap serializer.

Serializes the immutable DatavionOS runtime bootstrap payload.

Bootstrap is the single runtime contract consumed by
DatavionOS frontend applications.
"""

from __future__ import annotations

from rest_framework import serializers

from apps.datavionos.api.serializers.branding import (
    BrandingSerializer,
)
from apps.datavionos.api.serializers.dashboard import (
    DashboardCardSerializer,
)
from apps.datavionos.api.serializers.module import (
    ModuleContractSerializer,
)
from apps.datavionos.api.serializers.navigation import (
    NavigationItemSerializer,
)
from apps.datavionos.api.serializers.user import (
    BootstrapUserSerializer,
)


class TenantBootstrapSerializer(
    serializers.Serializer,
):
    """
    Tenant runtime information.
    """

    id = serializers.UUIDField(
        read_only=True,
    )

    name = serializers.CharField(
        read_only=True,
    )

    tenant_type = serializers.CharField(
        read_only=True,
    )

    status = serializers.CharField(
        read_only=True,
    )


class SubscriptionPlanSerializer(
    serializers.Serializer,
):
    """
    Subscription plan runtime information.
    """

    name = serializers.CharField(
        read_only=True,
    )

    code = serializers.CharField(
        read_only=True,
    )

    billing_cycle = serializers.CharField(
        read_only=True,
    )


class SubscriptionSerializer(
    serializers.Serializer,
):
    """
    Tenant subscription runtime information.
    """

    status = serializers.CharField(
        read_only=True,
    )

    auto_renew = serializers.BooleanField(
        read_only=True,
    )

    plan = SubscriptionPlanSerializer(
        read_only=True,
    )


class PlatformBootstrapSerializer(
    serializers.Serializer,
):
    """
    Serialize the DatavionOS runtime bootstrap contract.

    Provides:

    - Identity
    - Tenant
    - Organization
    - Employee
    - Platform RBAC
    - Organization RBAC
    - Effective permissions
    - Available modules
    - Navigation
    - Dashboard
    - Branding
    - Feature flags
    - Subscription
    - Preferences
    """

    user = BootstrapUserSerializer(
        source="context.user",
        read_only=True,
    )

    tenant = TenantBootstrapSerializer(
        source="context.tenant",
        allow_null=True,
        read_only=True,
    )

    organization = serializers.SerializerMethodField()

    employee = serializers.SerializerMethodField()

    # ==================================================================
    # RBAC
    # ==================================================================

    platform_roles = serializers.ListField(
        source="context.platform_roles",
        child=serializers.CharField(),
        read_only=True,
    )

    organization_roles = serializers.ListField(
        source="context.organization_roles",
        child=serializers.CharField(),
        read_only=True,
    )

    permissions = serializers.SerializerMethodField()

    # ==================================================================
    # Runtime Platform
    # ==================================================================

    modules = ModuleContractSerializer(
        many=True,
        read_only=True,
    )

    navigation = NavigationItemSerializer(
        many=True,
        read_only=True,
    )

    dashboard = DashboardCardSerializer(
        many=True,
        read_only=True,
    )

    branding = BrandingSerializer(
        read_only=True,
    )

    feature_flags = serializers.DictField(
        read_only=True,
    )

    subscription = SubscriptionSerializer(
        allow_null=True,
        read_only=True,
    )

    preferences = serializers.DictField(
        allow_null=True,
        required=False,
        read_only=True,
    )

    # ==================================================================
    # Computed Runtime Fields
    # ==================================================================

    def get_permissions(
        self,
        obj,
    ) -> list[str]:
        """
        Serialize effective permissions.

        Converts the immutable permission set into a stable,
        deterministic JSON list.
        """

        return sorted(
            obj.context.permissions,
        )

    def get_organization(
        self,
        obj,
    ) -> dict[str, object] | None:
        """
        Serialize organization runtime data.
        """

        organization = obj.context.organization

        if organization is None:
            return None

        return {
            "id": str(
                organization.id,
            ),
            "name": organization.name,
        }

    def get_employee(
        self,
        obj,
    ) -> dict[str, object] | None:
        """
        Serialize employee runtime data.
        """

        employee = obj.context.employee

        if employee is None:
            return None

        return {
            "id": str(
                employee.id,
            ),
            "employee_code": employee.employee_code,
        }


__all__ = (
    "TenantBootstrapSerializer",
    "SubscriptionPlanSerializer",
    "SubscriptionSerializer",
    "PlatformBootstrapSerializer",
)
