"""Read-only Finance Manager dashboard API."""

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.revenue_cycle.revenue_analytics.dashboard_service import (
    build_finance_dashboard,
)
from apps.revenue_cycle.revenue_analytics.policies import RevenueAnalyticsPolicy


class FinanceManagerDashboardAPIView(APIView):
    """Return live, organization-scoped revenue and collection metrics."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        tenant = getattr(request, "tenant", None)
        organization = getattr(request, "organization", None)
        if (
            tenant is None
            or organization is None
            or organization.tenant_id != tenant.id
        ):
            return Response(
                {"detail": "Explicit tenant and organization context is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not RevenueAnalyticsPolicy.can_list(
            user=request.user,
            organization=organization,
        ):
            return Response(
                {"detail": "You do not have permission to view revenue analytics."},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(build_finance_dashboard(organization=organization))


__all__ = ("FinanceManagerDashboardAPIView",)
