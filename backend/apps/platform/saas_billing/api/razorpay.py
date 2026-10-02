"""
Razorpay API endpoints for DatavionOS SaaS billing.

These endpoints do not trust payment status supplied by the browser.
"""

from __future__ import annotations

import json
from typing import Any

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from apps.platform.saas_billing.gateways import (
    RazorpaySaaSBillingService,
)
from apps.platform.saas_billing.models import Payment
from apps.platform.saas_billing.services.payment_service import PaymentService


def _settle_verified_payment(
    *, order_id: str, payment_id: str, payload: dict[str, Any]
):
    """Settle only a known pending Razorpay payment after signature verification."""
    payment = (
        Payment.objects.select_related("invoice__subscription")
        .filter(
            provider=Payment.Provider.RAZORPAY,
            gateway_order_id=order_id,
        )
        .first()
    )
    if payment is None:
        return None
    if payment.status == Payment.Status.SUCCESS:
        return payment
    payment.gateway_payment_id = payment_id
    payment.transaction_id = payment_id
    payment.save(update_fields=("gateway_payment_id", "transaction_id", "updated_at"))
    return PaymentService.mark_success(payment=payment, gateway_response=payload)


def _json_body(request) -> dict[str, Any]:
    try:
        return json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return {}


@require_http_methods(["POST"])
def verify_checkout(request):
    payload = _json_body(request)

    order_id = str(payload.get("razorpay_order_id", "")).strip()

    payment_id = str(payload.get("razorpay_payment_id", "")).strip()

    signature = str(payload.get("razorpay_signature", "")).strip()

    if not order_id or not payment_id or not signature:
        return JsonResponse(
            {
                "success": False,
                "error": "Incomplete Razorpay checkout response.",
            },
            status=400,
        )

    service = RazorpaySaaSBillingService()

    try:
        service.verify_checkout(
            order_id=order_id,
            payment_id=payment_id,
            signature=signature,
        )
    except Exception as exc:
        return JsonResponse(
            {
                "success": False,
                "error": str(exc),
            },
            status=400,
        )

    payment = _settle_verified_payment(
        order_id=order_id,
        payment_id=payment_id,
        payload=payload,
    )
    if payment is None:
        return JsonResponse(
            {"success": False, "error": "Payment order was not found."}, status=404
        )

    return JsonResponse(
        {
            "success": True,
            "verified": True,
            "razorpay_order_id": order_id,
            "razorpay_payment_id": payment_id,
        }
    )


@csrf_exempt
@require_http_methods(["POST"])
def webhook(request):
    signature = request.headers.get(
        "X-Razorpay-Signature",
        "",
    ).strip()

    if not signature:
        return JsonResponse(
            {
                "success": False,
                "error": "Missing Razorpay webhook signature.",
            },
            status=400,
        )

    service = RazorpaySaaSBillingService()

    try:
        service.verify_webhook(
            body=request.body,
            signature=signature,
        )
    except Exception as exc:
        return JsonResponse(
            {
                "success": False,
                "error": str(exc),
            },
            status=400,
        )

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse(
            {
                "success": False,
                "error": "Invalid webhook JSON.",
            },
            status=400,
        )

    event = str(payload.get("event", "")).strip()

    entity = payload.get("payload", {}).get("payment", {}).get("entity", {})
    order_id = str(entity.get("order_id", "")).strip()
    payment_id = str(entity.get("id", "")).strip()
    payment = None
    if event in {"payment.captured", "payment.authorized"} and order_id and payment_id:
        payment = _settle_verified_payment(
            order_id=order_id, payment_id=payment_id, payload=payload
        )
    elif event == "payment.failed" and order_id:
        payment = Payment.objects.filter(
            provider=Payment.Provider.RAZORPAY, gateway_order_id=order_id
        ).first()
        if payment and payment.status != Payment.Status.SUCCESS:
            PaymentService.mark_failed(
                payment=payment,
                reason=str(entity.get("error_description", "Gateway payment failed.")),
                gateway_response=payload,
            )

    return JsonResponse(
        {
            "success": True,
            "verified": True,
            "event": event,
            "reconciled": payment is not None,
        }
    )


# ---------------------------------------------------------------------------
# Canonical DatavionOS APIView adapters
# ---------------------------------------------------------------------------
#
# The existing verify_checkout() and webhook() functions remain the
# canonical business handlers. These APIViews provide the canonical
# class-based API boundary required by the SaaS Billing API contract.
#

from rest_framework.views import APIView


class RazorpayVerifyAPIView(APIView):
    """
    Canonical SaaS Billing Razorpay checkout verification endpoint.

    Delegates to the existing canonical verify_checkout() handler.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        return verify_checkout(request)


class RazorpayWebhookAPIView(APIView):
    """
    Canonical SaaS Billing Razorpay webhook endpoint.

    Delegates to the existing canonical webhook() handler.
    """

    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        return webhook(request)


__all__ = [
    "verify_checkout",
    "webhook",
    "RazorpayVerifyAPIView",
    "RazorpayWebhookAPIView",
]
