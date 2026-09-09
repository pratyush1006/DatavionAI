"""
Billing Core Insurance Claim API views.

HTTP orchestration for organization-scoped insurance claim operations.
"""

from __future__ import annotations

from decimal import Decimal
from uuid import UUID

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.billing.api.serializers import (
    InsuranceClaimApproveSerializer,
    InsuranceClaimCreateSerializer,
    InsuranceClaimDetailSerializer,
    InsuranceClaimListSerializer,
    InsuranceClaimRejectSerializer,
)
from apps.billing.api.views._base import BillingAPIViewMixin
from apps.billing.permissions import (
    CanApproveClaim,
    CanRejectClaim,
    CanSettleClaim,
    CanSubmitClaim,
    CanViewBilling,
)
from apps.billing.selectors import InsuranceClaimSelector
from apps.billing.workflows import (
    ClaimAppealWorkflow,
    ClaimApprovalWorkflow,
    ClaimCreationRequest,
    ClaimCreationWorkflow,
    ClaimRejectWorkflow,
    ClaimSettleWorkflow,
    ClaimTransitionRequest,
)


class InsuranceClaimListCreateAPIView(BillingAPIViewMixin, APIView):
    """List and submit organization-scoped insurance claims."""

    def get(self, request):
        """Return organization-scoped insurance claims."""
        organization = self.get_organization(request)

        CanViewBilling().has_permission(
            request,
            self,
        )

        records = InsuranceClaimSelector.list(
            tenant_id=organization.tenant_id,
            organization_id=organization.pk,
        )

        serializer = InsuranceClaimListSerializer(
            records,
            many=True,
        )

        return Response(serializer.data)

    def post(self, request):
        """Submit an insurance claim through the workflow boundary."""
        organization = self.get_organization(request)

        CanSubmitClaim().has_permission(
            request,
            self,
        )

        serializer = InsuranceClaimCreateSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        data = dict(serializer.validated_data)

        patient_id = data.pop("patient")
        invoice_id = data.pop("invoice")

        result = ClaimCreationWorkflow(
            request=ClaimCreationRequest(
                organization_id=organization.pk,
                patient_id=patient_id,
                invoice_id=invoice_id,
                data=data,
            ),
        ).run(
            context=self.workflow_context(
                request,
                "billing.claim.create",
            ),
        )

        return Response(
            InsuranceClaimDetailSerializer(
                result.data,
            ).data,
            status=status.HTTP_201_CREATED,
        )


class InsuranceClaimRetrieveUpdateAPIView(
    BillingAPIViewMixin,
    APIView,
):
    """Retrieve one organization-scoped insurance claim."""

    def get(
        self,
        request,
        claim_id: UUID,
    ):
        """Return one organization-scoped insurance claim."""
        organization = self.get_organization(request)

        CanViewBilling().has_permission(
            request,
            self,
        )

        claim = InsuranceClaimSelector.get(
            tenant_id=organization.tenant_id,
            organization_id=organization.pk,
            claim_id=claim_id,
        )

        return Response(
            InsuranceClaimDetailSerializer(
                claim,
            ).data,
        )


class InsuranceClaimApproveAPIView(
    BillingAPIViewMixin,
    APIView,
):
    """Approve an insurance claim."""

    def post(
        self,
        request,
        claim_id: UUID,
    ):
        """Approve an insurance claim through its workflow."""
        organization = self.get_organization(request)

        CanApproveClaim().has_permission(
            request,
            self,
        )

        serializer = InsuranceClaimApproveSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        result = ClaimApprovalWorkflow(
            request=ClaimTransitionRequest(
                organization_id=organization.pk,
                claim_id=claim_id,
            ),
            approved_amount=Decimal(
                str(
                    serializer.validated_data["approved_amount"],
                ),
            ),
        ).run(
            context=self.workflow_context(
                request,
                "billing.claim.approve",
            ),
        )

        return Response(
            InsuranceClaimDetailSerializer(
                result.data,
            ).data,
        )


class InsuranceClaimRejectAPIView(
    BillingAPIViewMixin,
    APIView,
):
    """Reject an insurance claim."""

    def post(
        self,
        request,
        claim_id: UUID,
    ):
        """Reject an insurance claim through its workflow."""
        organization = self.get_organization(request)

        CanRejectClaim().has_permission(
            request,
            self,
        )

        serializer = InsuranceClaimRejectSerializer(
            data=request.data,
        )
        serializer.is_valid(
            raise_exception=True,
        )

        result = ClaimRejectWorkflow(
            request=ClaimTransitionRequest(
                organization_id=organization.pk,
                claim_id=claim_id,
            ),
            rejection_reason=serializer.validated_data["rejection_reason"],
        ).run(
            context=self.workflow_context(
                request,
                "billing.claim.reject",
            ),
        )

        return Response(
            InsuranceClaimDetailSerializer(
                result.data,
            ).data,
        )


class InsuranceClaimAppealAPIView(
    BillingAPIViewMixin,
    APIView,
):
    """Appeal a rejected insurance claim."""

    def post(
        self,
        request,
        claim_id: UUID,
    ):
        """Appeal a rejected insurance claim through its workflow."""
        organization = self.get_organization(request)

        CanApproveClaim().has_permission(
            request,
            self,
        )

        result = ClaimAppealWorkflow(
            request=ClaimTransitionRequest(
                organization_id=organization.pk,
                claim_id=claim_id,
            ),
        ).run(
            context=self.workflow_context(
                request,
                "billing.claim.appeal",
            ),
        )

        return Response(
            InsuranceClaimDetailSerializer(
                result.data,
            ).data,
        )


class InsuranceClaimSettleAPIView(
    BillingAPIViewMixin,
    APIView,
):
    """Settle an approved insurance claim."""

    def post(
        self,
        request,
        claim_id: UUID,
    ):
        """Settle an approved insurance claim through its workflow."""
        organization = self.get_organization(request)

        CanSettleClaim().has_permission(
            request,
            self,
        )

        result = ClaimSettleWorkflow(
            request=ClaimTransitionRequest(
                organization_id=organization.pk,
                claim_id=claim_id,
            ),
        ).run(
            context=self.workflow_context(
                request,
                "billing.claim.settle",
            ),
        )

        return Response(
            InsuranceClaimDetailSerializer(
                result.data,
            ).data,
        )


__all__ = (
    "InsuranceClaimAppealAPIView",
    "InsuranceClaimApproveAPIView",
    "InsuranceClaimListCreateAPIView",
    "InsuranceClaimRejectAPIView",
    "InsuranceClaimRetrieveUpdateAPIView",
    "InsuranceClaimSettleAPIView",
)
