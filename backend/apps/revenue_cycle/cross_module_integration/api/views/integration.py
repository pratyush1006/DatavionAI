"""DRF views for Revenue Cycle cross-module integration."""

from __future__ import annotations

from uuid import UUID

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ...constants import (
    IntegrationEventType,
    IntegrationRecordStatus,
    IntegrationSource,
)
from ...policies import CrossModuleIntegrationPolicy
from ...selectors import CrossModuleIntegrationSelector
from ...workflows import CrossModuleIntegrationWorkflow
from ..serializers import RevenueCycleIntegrationRecordSerializer


def _context(request):
    """Require explicit tenant and organization context."""

    tenant = request.tenant
    organization = request.organization
    if organization.tenant_id != tenant.id:
        raise PermissionError("Organization does not belong to the active tenant.")
    return tenant, organization


class RevenueCycleIntegrationListAPIView(APIView):
    """List organization-scoped integration records."""

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        """Return filtered integration records."""

        _, organization = _context(request)
        if not CrossModuleIntegrationPolicy.can_list(
            user=request.user,
            organization=organization,
        ):
            return Response(status=status.HTTP_403_FORBIDDEN)

        status_filter = request.query_params.get("status")
        source_filter = request.query_params.get("source")

        if status_filter and status_filter not in IntegrationRecordStatus.values:
            return Response(
                {"detail": "Unsupported integration status."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if source_filter and source_filter not in IntegrationSource.values:
            return Response(
                {"detail": "Unsupported integration source."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        records = CrossModuleIntegrationSelector.records(
            organization_id=organization.id,
            status=status_filter,
            source=source_filter,
        )
        return Response(
            RevenueCycleIntegrationRecordSerializer(
                records,
                many=True,
            ).data
        )


class RevenueCycleIntegrationIngestAPIView(APIView):
    """Ingest a cross-module integration event."""

    permission_classes = (IsAuthenticated,)

    def post(self, request):
        """Ingest an integration envelope through the workflow layer."""

        _, organization = _context(request)
        serializer = RevenueCycleIntegrationRecordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event_type = serializer.validated_data["event_type"]
        source = serializer.validated_data["source"]

        if event_type not in IntegrationEventType.values:
            return Response(
                {"detail": "Unsupported integration event type."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if source not in IntegrationSource.values:
            return Response(
                {"detail": "Unsupported integration source."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            result = CrossModuleIntegrationWorkflow.ingest(
                user=request.user,
                organization=organization,
                event_type=event_type,
                source=source,
                event_name=serializer.validated_data["event_name"],
                aggregate_id=serializer.validated_data["aggregate_id"],
                idempotency_key=serializer.validated_data["idempotency_key"],
                payload=serializer.validated_data["payload"],
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
            RevenueCycleIntegrationRecordSerializer(result).data,
            status=status.HTTP_201_CREATED,
        )


class RevenueCycleIntegrationProcessAPIView(APIView):
    """Process a pending cross-module integration record."""

    permission_classes = (IsAuthenticated,)

    def post(self, request, record_id: UUID):
        """Process an integration record through the workflow layer."""

        _, organization = _context(request)
        try:
            result = CrossModuleIntegrationWorkflow.process(
                user=request.user,
                organization=organization,
                record_id=record_id,
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
        except RevenueCycleIntegrationRecord.DoesNotExist:
            return Response(
                {"detail": "Integration record not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            RevenueCycleIntegrationRecordSerializer(result).data,
            status=status.HTTP_200_OK,
        )


__all__ = (
    "RevenueCycleIntegrationIngestAPIView",
    "RevenueCycleIntegrationListAPIView",
    "RevenueCycleIntegrationProcessAPIView",
)
