"""
SaaS Billing Usage API views.

Handles:

- Usage listing
- Usage collection
- Usage evaluation
- Usage charging

Architecture:

API
 |
Organization Context
 |
RBAC
 |
Serializer
 |
Workflow Registry
 |
Usage Workflow
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import (
    success_response,
)
from apps.platform.saas_billing.api.mixins import (
    OrganizationContextMixin,
)
from apps.platform.saas_billing.api.permissions import (
    CanManageUsage,
    CanViewUsage,
)
from apps.platform.saas_billing.api.serializers import (
    UsageChargeSerializer,
    UsageCreateSerializer,
    UsageEvaluationSerializer,
    UsageSerializer,
)
from apps.platform.saas_billing.models import (
    Usage,
)
from apps.platform.saas_billing.workflows import (
    WorkflowRegistry,
)


class UsageListAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    List organization usage.

    GET /billing/usage/
    """

    permission_classes = [
        CanViewUsage,
    ]

    def get(
        self,
        request,
    ):
        """
        Return usage records.
        """

        usage_records = Usage.objects.filter(
            organization=self.get_organization(
                request,
            ),
        ).order_by(
            "-created_at",
        )

        return success_response(
            data=UsageSerializer(
                usage_records,
                many=True,
            ).data,
        )


class UsageCollectAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Collect usage record.

    POST /billing/usage/collect/
    """

    permission_classes = [
        CanManageUsage,
    ]

    def post(
        self,
        request,
    ):
        """
        Execute usage collection workflow.
        """

        serializer = UsageCreateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        usage = WorkflowRegistry.execute(
            "usage.collect",
            organization=(
                self.get_organization(
                    request,
                )
            ),
            metric_type=(serializer.validated_data["metric_type"]),
            value=(serializer.validated_data["value"]),
            module=(
                serializer.validated_data.get(
                    "module",
                )
            ),
            source=(
                serializer.validated_data.get(
                    "source",
                )
            ),
            reference_id=(
                serializer.validated_data.get(
                    "reference_id",
                )
            ),
            billable=(
                serializer.validated_data.get(
                    "billable",
                    False,
                )
            ),
        )

        return success_response(
            data=UsageSerializer(
                usage,
            ).data,
            status_code=status.HTTP_201_CREATED,
        )


class UsageEvaluateAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Evaluate usage limits.

    POST /billing/usage/<id>/evaluate/
    """

    permission_classes = [
        CanManageUsage,
    ]

    def post(
        self,
        request,
        pk,
    ):

        usage = Usage.objects.filter(
            organization=self.get_organization(
                request,
            ),
            id=pk,
        ).first()

        if not usage:
            return Response(
                {"detail": ("Usage record not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UsageEvaluationSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        usage = WorkflowRegistry.execute(
            "usage.evaluate",
            usage=usage,
        )

        return success_response(
            data=UsageSerializer(
                usage,
            ).data,
        )


class UsageChargeAPIView(
    OrganizationContextMixin,
    APIView,
):
    """
    Calculate usage charge.

    POST /billing/usage/<id>/charge/
    """

    permission_classes = [
        CanManageUsage,
    ]

    def post(
        self,
        request,
        pk,
    ):

        usage = Usage.objects.filter(
            organization=self.get_organization(
                request,
            ),
            id=pk,
        ).first()

        if not usage:
            return Response(
                {"detail": ("Usage record not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UsageChargeSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        usage = WorkflowRegistry.execute(
            "usage.charge",
            usage=usage,
            rate=(serializer.validated_data["billing_rate"]),
        )

        return success_response(
            data=UsageSerializer(
                usage,
            ).data,
        )


__all__ = (
    "UsageListAPIView",
    "UsageCollectAPIView",
    "UsageEvaluateAPIView",
    "UsageChargeAPIView",
)
