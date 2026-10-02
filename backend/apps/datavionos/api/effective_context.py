"""Effective capability API boundary.

Canonical DatavionOS runtime capability API.

Runtime authority:

    User
      -> TenantMembership
      -> Tenant
      -> Organization
      -> Subscription
      -> Plan
      -> Entitlement
      -> RBAC
      -> Effective Capability
      -> API
      -> Dashboard / Navigation

This API does not independently calculate dashboard eligibility.
All entitlement and RBAC decisions are delegated to the canonical
SaaS capability provider and the canonical effective capability builder.
"""

from __future__ import annotations

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.datavionos.services.effective_capability import (
    build_effective_capability_context,
)
from apps.datavionos.services.saas_capability_control_plane import (
    get_provider,
)


class EffectiveCapabilityContextAPIView(APIView):
    """Expose the canonical effective capability context."""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        organization = getattr(request, "organization", None)

        if organization is None:
            organization = getattr(request.user, "organization", None)

        if organization is None:
            return Response(
                {
                    "success": False,
                    "status": "error",
                    "error": {
                        "code": "ACTIVE_ORGANIZATION_REQUIRED",
                        "message": "Active organization is required.",
                    },
                },
                status=400,
            )

        provider = get_provider()

        snapshot = provider.resolve(
            user=request.user,
            organization=organization,
        )

        context = build_effective_capability_context(
            user_id=str(snapshot.user_id or getattr(request.user, "pk", "")),
            organization_id=str(
                snapshot.organization_id or getattr(organization, "pk", "")
            ),
            tenant_id=snapshot.tenant_id,
            modules=snapshot.modules,
            features=snapshot.features,
            permissions=snapshot.permissions,
            roles=getattr(snapshot, "roles", frozenset()),
            facilities=getattr(snapshot, "facilities", frozenset()),
            departments=getattr(snapshot, "departments", frozenset()),
            data_scopes=getattr(snapshot, "data_scopes", {}),
            ai_capabilities=getattr(
                snapshot,
                "ai_capabilities",
                {},
            ),
            limits=getattr(snapshot, "limits", {}),
        )

        effective_capabilities = context.as_dict()

        modules = dict(context.modules)

        response_data = {
            "success": True,
            "status": "success",
            # -----------------------------------------------------------------
            # Backward-compatible top-level contract.
            # -----------------------------------------------------------------
            "user_id": context.user_id,
            "organization_id": context.organization_id,
            "tenant_id": context.tenant_id,
            "modules": modules,
            "module_state": modules,
            "features": dict(context.features),
            "permissions": sorted(context.permissions),
            "roles": sorted(context.roles),
            "facilities": sorted(context.facilities),
            "departments": sorted(context.departments),
            "data_scopes": dict(context.data_scopes),
            "ai_capabilities": dict(context.ai_capabilities),
            "limits": dict(context.limits),
            # -----------------------------------------------------------------
            # Canonical nested capability contract.
            # -----------------------------------------------------------------
            "capabilities": {
                "effective_capabilities": effective_capabilities,
            },
            # -----------------------------------------------------------------
            # Explicit runtime aliases used by frontend/runtime consumers.
            # -----------------------------------------------------------------
            "effective_capabilities": effective_capabilities,
        }

        return Response(response_data)
