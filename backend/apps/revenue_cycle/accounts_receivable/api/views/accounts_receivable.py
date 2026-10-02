"""DRF views for Revenue Cycle Accounts Receivable."""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from django.shortcuts import get_object_or_404
from django.utils.dateparse import parse_datetime
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.openapi import extend_schema

from ...policies import ARPolicy
from ...selectors import ARSelector
from ...workflows import ARWorkflow
from ..serializers import (
    ARAccountHoldSerializer,
    ARAccountSerializer,
    ARAccountWriteOffSerializer,
    ARTransactionSerializer,
)


def _context(request):
    """Require explicit tenant and organization context."""

    tenant = request.tenant
    organization = request.organization
    if organization.tenant_id != tenant.id:
        raise PermissionError("Organization does not belong to the active tenant.")
    return tenant, organization


class ARAccountListAPIView(APIView):
    """List organization-scoped Accounts Receivable accounts."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=ARAccountSerializer(many=True))
    def get(self, request):
        """Return organization-scoped AR accounts."""

        _, organization = _context(request)
        if not ARPolicy.can_list(user=request.user, organization=organization):
            return Response(status=status.HTTP_403_FORBIDDEN)
        queryset = ARSelector.accounts(organization_id=organization.id)
        return Response(ARAccountSerializer(queryset, many=True).data)


class ARTransactionListCreateAPIView(APIView):
    """List or post Accounts Receivable transactions."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=ARTransactionSerializer(many=True))
    def get(self, request, account_id: UUID):
        """Return transactions for one organization-scoped account."""

        _, organization = _context(request)
        if not ARPolicy.can_list(user=request.user, organization=organization):
            return Response(status=status.HTTP_403_FORBIDDEN)
        account = get_object_or_404(
            ARSelector.accounts(organization_id=organization.id),
            id=account_id,
        )
        queryset = ARSelector.transactions(
            organization_id=organization.id,
            account_id=account.id,
        )
        return Response(ARTransactionSerializer(queryset, many=True).data)

    @extend_schema(
        request=ARTransactionSerializer,
        responses={status.HTTP_201_CREATED: ARTransactionSerializer},
    )
    def post(self, request, account_id: UUID):
        """Post a new AR transaction through the workflow layer."""

        _, organization = _context(request)
        serializer = ARTransactionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        transaction_date = parse_datetime(
            request.data.get("transaction_date", ""),
        )
        if transaction_date is None:
            return Response(
                {"detail": "transaction_date must be a valid ISO datetime."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            result = ARWorkflow.post_transaction(
                user=request.user,
                organization=organization,
                account_id=account_id,
                transaction_type=serializer.validated_data["transaction_type"],
                amount=Decimal(serializer.validated_data["amount"]),
                transaction_number=serializer.validated_data["transaction_number"],
                transaction_date=transaction_date,
                source_type=serializer.validated_data.get("source_type", ""),
                source_id=serializer.validated_data.get("source_id"),
                external_reference=serializer.validated_data.get(
                    "external_reference",
                    "",
                ),
                note=serializer.validated_data.get("note", ""),
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
            ARTransactionSerializer(result).data,
            status=status.HTTP_201_CREATED,
        )


class ARTransactionReverseAPIView(APIView):
    """Reverse a posted Accounts Receivable transaction."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=ARTransactionSerializer)
    def post(self, request, transaction_id: UUID):
        """Reverse an AR transaction through the workflow layer."""

        _, organization = _context(request)
        try:
            result = ARWorkflow.reverse_transaction(
                user=request.user,
                organization=organization,
                transaction_id=transaction_id,
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
        return Response(ARTransactionSerializer(result).data)


class ARAccountHoldAPIView(APIView):
    """Place an Accounts Receivable account on hold."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=ARAccountHoldSerializer,
        responses=ARAccountSerializer,
    )
    def post(self, request, account_id: UUID):
        """Place the account on hold through the workflow layer."""

        _, organization = _context(request)
        try:
            result = ARWorkflow.hold(
                user=request.user,
                organization=organization,
                account_id=account_id,
                reason=request.data.get("reason", ""),
                note=request.data.get("note", ""),
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
        return Response(ARAccountSerializer(result).data)


class ARAccountHoldReleaseAPIView(APIView):
    """Release an Accounts Receivable account hold."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(responses=ARAccountSerializer)
    def post(self, request, account_id: UUID):
        """Release the account hold through the workflow layer."""

        _, organization = _context(request)
        try:
            result = ARWorkflow.release_hold(
                user=request.user,
                organization=organization,
                account_id=account_id,
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
        return Response(ARAccountSerializer(result).data)


class ARAccountWriteOffAPIView(APIView):
    """Write off the outstanding balance of an AR account."""

    permission_classes = (IsAuthenticated,)

    @extend_schema(
        request=ARAccountWriteOffSerializer,
        responses={status.HTTP_201_CREATED: ARTransactionSerializer},
    )
    def post(self, request, account_id: UUID):
        """Write off the account balance through the workflow layer."""

        _, organization = _context(request)
        try:
            result = ARWorkflow.write_off(
                user=request.user,
                organization=organization,
                account_id=account_id,
                transaction_number=request.data.get("transaction_number", ""),
                note=request.data.get("note", ""),
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
            ARTransactionSerializer(result).data,
            status=status.HTTP_201_CREATED,
        )


__all__ = (
    "ARAccountHoldAPIView",
    "ARAccountHoldReleaseAPIView",
    "ARAccountListAPIView",
    "ARAccountWriteOffAPIView",
    "ARTransactionListCreateAPIView",
    "ARTransactionReverseAPIView",
)
