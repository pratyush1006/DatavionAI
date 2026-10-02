"""DRF views for Revenue Analytics."""

from __future__ import annotations

from decimal import Decimal

from django.utils.dateparse import parse_date
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ...constants import AnalyticsPeriod
from ...policies import RevenueAnalyticsPolicy
from ...selectors import RevenueAnalyticsSelector
from ...workflows import RevenueAnalyticsWorkflow
from ..serializers import RevenueMetricSnapshotSerializer


def _context(request):
    """Require explicit tenant and organization context."""

    tenant = request.tenant
    organization = request.organization
    if organization.tenant_id != tenant.id:
        raise PermissionError("Organization does not belong to the active tenant.")
    return tenant, organization


def _decimal(data, field_name: str) -> Decimal:
    """Parse a non-negative decimal request field."""

    try:
        value = Decimal(str(data.get(field_name, "0")))
    except Exception as exc:
        raise ValueError(f"{field_name} must be a valid decimal.") from exc
    if value < 0:
        raise ValueError(f"{field_name} cannot be negative.")
    return value


def _count(data, field_name: str) -> int:
    """Parse a non-negative integer request field."""

    try:
        value = int(data.get(field_name, 0))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"{field_name} must be a valid integer.") from exc
    if value < 0:
        raise ValueError(f"{field_name} cannot be negative.")
    return value


class RevenueAnalyticsListAPIView(APIView):
    """List organization-scoped Revenue Analytics snapshots."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return filtered analytics snapshots."""

        _, organization = _context(request)
        if not RevenueAnalyticsPolicy.can_list(
            user=request.user,
            organization=organization,
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        start_date = request.query_params.get("start_date")
        end_date = request.query_params.get("end_date")
        period = request.query_params.get("period")

        parsed_start = parse_date(start_date) if start_date else None
        parsed_end = parse_date(end_date) if end_date else None

        if start_date and parsed_start is None:
            return Response(
                {"detail": "start_date must be a valid ISO date."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if end_date and parsed_end is None:
            return Response(
                {"detail": "end_date must be a valid ISO date."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if period and period not in AnalyticsPeriod.values:
            return Response(
                {"detail": "Unsupported analytics period."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        queryset = RevenueAnalyticsSelector.snapshots(
            organization_id=organization.id,
            period=period,
            start_date=parsed_start,
            end_date=parsed_end,
        )
        return Response(
            RevenueMetricSnapshotSerializer(queryset, many=True).data,
        )


class RevenueAnalyticsGenerateAPIView(APIView):
    """Generate one organization-scoped analytics snapshot."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Generate a snapshot through RBAC and workflow layers."""

        _, organization = _context(request)
        payload = request.data
        period = payload.get("period", "")
        period_start = parse_date(payload.get("period_start", ""))
        period_end = parse_date(payload.get("period_end", ""))

        if period not in AnalyticsPeriod.values:
            return Response(
                {"detail": "Unsupported analytics period."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if period_start is None or period_end is None:
            return Response(
                {"detail": "period_start and period_end must be valid ISO dates."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = RevenueAnalyticsWorkflow.generate(
                user=request.user,
                organization=organization,
                period=period,
                period_start=period_start,
                period_end=period_end,
                gross_charges=_decimal(payload, "gross_charges"),
                payments=_decimal(payload, "payments"),
                adjustments=_decimal(payload, "adjustments"),
                denials=_decimal(payload, "denials"),
                write_offs=_decimal(payload, "write_offs"),
                outstanding_ar=_decimal(payload, "outstanding_ar"),
                encounter_count=_count(payload, "encounter_count"),
                claim_count=_count(payload, "claim_count"),
                denied_claim_count=_count(payload, "denied_claim_count"),
                paid_claim_count=_count(payload, "paid_claim_count"),
            )
        except PermissionError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_403_FORBIDDEN,
            )
        except ValueError as exc:
            return Response(
                {"detail": str(exc)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            RevenueMetricSnapshotSerializer(result).data,
            status=status.HTTP_201_CREATED,
        )


__all__ = (
    "RevenueAnalyticsGenerateAPIView",
    "RevenueAnalyticsListAPIView",
)
