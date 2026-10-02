"""
SaaS Billing Account API views.

Handles:

- Billing account retrieval
- Billing profile updates
- Payment provider configuration
- Auto charge configuration

Architecture:

API
 |
RBAC
 |
Serializer
 |
Service
 |
Model
"""

from __future__ import annotations

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.common.api.responses import (
    success_response,
)
from apps.platform.saas_billing.api.permissions import (
    CanManageBilling,
    CanViewBilling,
)
from apps.platform.saas_billing.api.serializers import (
    BillingAccountSerializer,
    BillingAccountUpdateSerializer,
)
from apps.platform.saas_billing.models import (
    BillingAccount,
)
from apps.platform.saas_billing.services import (
    BillingAccountService,
)


class BillingAccountDetailAPIView(
    APIView,
):
    """
    Retrieve organization billing account.

    GET /billing/account/
    """

    permission_classes = [
        CanViewBilling,
    ]

    def get(
        self,
        request,
    ):
        """
        Return billing account.
        """

        organization = getattr(
            request,
            "organization",
            None,
        )

        billing_account = BillingAccount.objects.filter(
            organization=organization,
        ).first()

        if not billing_account:
            return Response(
                {"detail": ("Billing account not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BillingAccountSerializer(
            billing_account,
        )

        return success_response(
            data=serializer.data,
        )


class BillingAccountUpdateAPIView(
    APIView,
):
    """
    Update billing profile.

    PATCH /billing/account/
    """

    permission_classes = [
        CanManageBilling,
    ]

    def patch(
        self,
        request,
    ):
        """
        Update billing profile.
        """

        organization = getattr(
            request,
            "organization",
            None,
        )

        billing_account = BillingAccount.objects.filter(
            organization=organization,
        ).first()

        if not billing_account:
            return Response(
                {"detail": ("Billing account not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BillingAccountUpdateSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        billing_account = BillingAccountService.update_billing_profile(
            billing_account=billing_account,
            data=serializer.validated_data,
        )

        return success_response(
            data=BillingAccountSerializer(
                billing_account,
            ).data,
        )


class BillingPaymentProviderAPIView(
    APIView,
):
    """
    Configure payment provider.

    PATCH /billing/account/payment-provider/
    """

    permission_classes = [
        CanManageBilling,
    ]

    def patch(
        self,
        request,
    ):
        """
        Configure gateway provider.
        """

        organization = getattr(
            request,
            "organization",
            None,
        )

        billing_account = BillingAccount.objects.filter(
            organization=organization,
        ).first()

        if not billing_account:
            return Response(
                {"detail": ("Billing account not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        billing_account = BillingAccountService.configure_payment_provider(
            billing_account=billing_account,
            provider=request.data.get(
                "provider",
                "",
            ),
            customer_id=request.data.get(
                "customer_id",
            ),
            payment_method_id=request.data.get(
                "payment_method_id",
            ),
        )

        return success_response(
            data=BillingAccountSerializer(
                billing_account,
            ).data,
        )


class BillingAutoChargeAPIView(
    APIView,
):
    """
    Enable or disable automatic charging.

    PATCH /billing/account/auto-charge/
    """

    permission_classes = [
        CanManageBilling,
    ]

    def patch(
        self,
        request,
    ):
        """
        Toggle automatic collection.
        """

        organization = getattr(
            request,
            "organization",
            None,
        )

        billing_account = BillingAccount.objects.filter(
            organization=organization,
        ).first()

        if not billing_account:
            return Response(
                {"detail": ("Billing account not found.")},
                status=status.HTTP_404_NOT_FOUND,
            )

        enabled = request.data.get(
            "enabled",
            False,
        )

        if enabled:
            billing_account = BillingAccountService.enable_auto_charge(
                billing_account=billing_account,
            )

        else:
            billing_account = BillingAccountService.disable_auto_charge(
                billing_account=billing_account,
            )

        return success_response(
            data=BillingAccountSerializer(
                billing_account,
            ).data,
        )


__all__ = (
    "BillingAccountDetailAPIView",
    "BillingAccountUpdateAPIView",
    "BillingPaymentProviderAPIView",
    "BillingAutoChargeAPIView",
)
