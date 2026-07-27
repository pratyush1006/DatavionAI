"""
API views for insurance claims.
"""

from __future__ import annotations

from typing import Final

from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.billing.api.serializers import (
    InsuranceClaimApproveSerializer,
    InsuranceClaimCreateSerializer,
    InsuranceClaimDetailSerializer,
    InsuranceClaimListSerializer,
    InsuranceClaimRejectSerializer,
    InsuranceClaimUpdateSerializer,
)
from apps.billing.models import InsuranceClaim
from apps.billing.permissions import (
    CanApproveClaim,
    CanSubmitClaim,
    CanViewInvoice,
)
from apps.billing.selectors import InsuranceClaimSelector
from apps.billing.services import InsuranceClaimService
from apps.common.api.responses import (
    error_response,
    success_response,
)
from apps.common.permissions import IsAuthenticatedAndActive

CLAIM_TAG: Final[tuple[str, ...]] = ("Insurance Claims",)


@extend_schema(tags=CLAIM_TAG)
class InsuranceClaimListCreateAPIView(APIView):
    """
    API view for listing and creating insurance claims.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    def get_permissions(
        self,
    ):
        """
        Return permissions for the current request.
        """

        if self.request.method == "POST":
            return [
                IsAuthenticated(),
                CanSubmitClaim(),
            ]

        return [
            IsAuthenticated(),
            CanViewInvoice(),
        ]

    def get(
        self,
        request: Request,
    ) -> Response:
        """
        List insurance claims.
        """

        queryset = InsuranceClaimSelector.queryset()

        page = self.paginate_queryset(
            queryset,
        )

        if page is not None:
            serializer = InsuranceClaimListSerializer(
                page,
                many=True,
            )

            return self.get_paginated_response(
                serializer.data,
            )

        serializer = InsuranceClaimListSerializer(
            queryset,
            many=True,
        )

        return success_response(
            data=serializer.data,
        )

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create an insurance claim.
        """

        serializer = InsuranceClaimCreateSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        claim = serializer.save(
            performed_by=request.user,
        )

        response_serializer = InsuranceClaimDetailSerializer(
            claim,
        )

        return success_response(
            message="Insurance claim submitted successfully.",
            data=response_serializer.data,
            status_code=201,
        )


@extend_schema(tags=CLAIM_TAG)
class InsuranceClaimRetrieveUpdateAPIView(APIView):
    """
    Retrieve or update an insurance claim.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    def get_permissions(
        self,
    ):
        """
        Return permissions for the current request.
        """

        method = self.request.method

        if method in ("PUT", "PATCH"):
            return [
                IsAuthenticated(),
                CanApproveClaim(),
            ]

        return [
            IsAuthenticated(),
            CanViewInvoice(),
        ]

    def get_object(
        self,
        claim_id: str,
    ) -> InsuranceClaim:
        """
        Return the requested claim.
        """

        return InsuranceClaimSelector.get(
            claim_id=claim_id,
        )

    def get(
        self,
        request: Request,
        claim_id: str,
    ) -> Response:
        """
        Retrieve an insurance claim.
        """

        claim = self.get_object(
            claim_id=claim_id,
        )

        serializer = InsuranceClaimDetailSerializer(
            claim,
        )

        return success_response(
            data=serializer.data,
        )

    def put(
        self,
        request: Request,
        claim_id: str,
    ) -> Response:
        """
        Update an insurance claim.
        """

        claim = self.get_object(
            claim_id=claim_id,
        )

        serializer = InsuranceClaimUpdateSerializer(
            instance=claim,
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        updated_claim = serializer.save()

        response_serializer = InsuranceClaimDetailSerializer(
            updated_claim,
        )

        return success_response(
            message="Insurance claim updated successfully.",
            data=response_serializer.data,
        )

    def patch(
        self,
        request: Request,
        claim_id: str,
    ) -> Response:
        """
        Partially update an insurance claim.
        """

        claim = self.get_object(
            claim_id=claim_id,
        )

        serializer = InsuranceClaimUpdateSerializer(
            instance=claim,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        updated_claim = serializer.save()

        response_serializer = InsuranceClaimDetailSerializer(
            updated_claim,
        )

        return success_response(
            message="Insurance claim updated successfully.",
            data=response_serializer.data,
        )


@extend_schema(tags=CLAIM_TAG)
class InsuranceClaimApproveAPIView(APIView):
    """
    Approve an insurance claim.
    """

    permission_classes = (IsAuthenticated, CanApproveClaim)

    def post(
        self,
        request: Request,
        claim_id: str,
    ) -> Response:
        """
        Approve an insurance claim.
        """

        claim = InsuranceClaimSelector.get(
            claim_id=claim_id,
        )

        serializer = InsuranceClaimApproveSerializer(
            data=request.data,
            context={"claim": claim},
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        approved_claim = InsuranceClaimService.approve(
            instance=claim,
            approved_amount=serializer.validated_data["approved_amount"],
            performed_by=request.user,
        )

        response_serializer = InsuranceClaimDetailSerializer(
            approved_claim,
        )

        return success_response(
            message="Insurance claim approved successfully.",
            data=response_serializer.data,
        )


@extend_schema(tags=CLAIM_TAG)
class InsuranceClaimRejectAPIView(APIView):
    """
    Reject an insurance claim.
    """

    permission_classes = (IsAuthenticated, CanApproveClaim)

    def post(
        self,
        request: Request,
        claim_id: str,
    ) -> Response:
        """
        Reject an insurance claim.
        """

        claim = InsuranceClaimSelector.get(
            claim_id=claim_id,
        )

        serializer = InsuranceClaimRejectSerializer(
            data=request.data,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        rejected_claim = InsuranceClaimService.reject(
            instance=claim,
            rejection_reason=serializer.validated_data["rejection_reason"],
            performed_by=request.user,
        )

        response_serializer = InsuranceClaimDetailSerializer(
            rejected_claim,
        )

        return success_response(
            message="Insurance claim rejected successfully.",
            data=response_serializer.data,
        )


@extend_schema(tags=CLAIM_TAG)
class InsuranceClaimBulkCreateAPIView(APIView):
    """
    Bulk create insurance claims.
    """

    permission_classes = (IsAuthenticatedAndActive,)

    def post(
        self,
        request: Request,
    ) -> Response:
        """
        Create multiple insurance claims.
        """

        if not isinstance(request.data, list):
            return error_response(
                message="Expected a list of claims.",
                status_code=400,
            )

        serializer = InsuranceClaimCreateSerializer(
            data=request.data,
            many=True,
        )

        if not serializer.is_valid():
            return error_response(
                details=serializer.errors,
            )

        claims = InsuranceClaimService.bulk_create(
            validated_data_list=serializer.validated_data,
            performed_by=request.user,
        )

        response_serializer = InsuranceClaimDetailSerializer(
            claims,
            many=True,
        )

        return success_response(
            message="Insurance claims created successfully.",
            data=response_serializer.data,
            status_code=201,
        )


__all__ = [
    "InsuranceClaimApproveAPIView",
    "InsuranceClaimBulkCreateAPIView",
    "InsuranceClaimListCreateAPIView",
    "InsuranceClaimRejectAPIView",
    "InsuranceClaimRetrieveUpdateAPIView",
]
