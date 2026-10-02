"""
Canonical Razorpay gateway adapter.

The adapter intentionally uses Python standard-library HTTP primitives
so the installer does not add a runtime dependency.

Razorpay secrets never leave the backend.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
from decimal import Decimal
from typing import Any
from urllib import error as urllib_error
from urllib import request as urllib_request

from ..razorpay_config import (
    RAZORPAY_CURRENCY,
    RAZORPAY_ENABLED,
    RAZORPAY_KEY_ID,
    RAZORPAY_KEY_SECRET,
    RAZORPAY_WEBHOOK_SECRET,
)
from .exceptions import (
    RazorpayAPIError,
    RazorpayConfigurationError,
    RazorpaySignatureError,
    RazorpayWebhookSignatureError,
)

RAZORPAY_API_BASE = "https://api.razorpay.com/v1"


class RazorpayGateway:
    """
    Thin, canonical Razorpay gateway.

    Amounts are accepted as INR decimal rupees and converted to paise
    only at the external Razorpay boundary.
    """

    def __init__(self) -> None:
        if not RAZORPAY_ENABLED:
            raise RazorpayConfigurationError("Razorpay integration is disabled.")

        if not RAZORPAY_KEY_ID:
            raise RazorpayConfigurationError("RAZORPAY_KEY_ID is not configured.")

        if not RAZORPAY_KEY_SECRET:
            raise RazorpayConfigurationError("RAZORPAY_KEY_SECRET is not configured.")

    @staticmethod
    def amount_to_paise(amount: Decimal | int | float | str) -> int:
        value = Decimal(str(amount))

        if value < Decimal("0"):
            raise ValueError("Payment amount cannot be negative.")

        return int((value * Decimal("100")).quantize(Decimal("1")))

    def _authorization_header(self) -> str:
        token = base64.b64encode(
            f"{RAZORPAY_KEY_ID}:{RAZORPAY_KEY_SECRET}".encode()
        ).decode("ascii")

        return f"Basic {token}"

    def _request(
        self,
        *,
        method: str,
        path: str,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        body = None

        if payload is not None:
            body = json.dumps(
                payload,
                separators=(",", ":"),
            ).encode("utf-8")

        request = urllib_request.Request(
            f"{RAZORPAY_API_BASE}{path}",
            data=body,
            method=method.upper(),
            headers={
                "Authorization": self._authorization_header(),
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
        )

        try:
            with urllib_request.urlopen(
                request,
                timeout=30,
            ) as response:
                raw = response.read().decode("utf-8")

        except urllib_error.HTTPError as exc:
            detail = exc.read().decode(
                "utf-8",
                errors="replace",
            )

            raise RazorpayAPIError(
                f"Razorpay API returned HTTP {exc.code}: {detail}"
            ) from exc

        except urllib_error.URLError as exc:
            raise RazorpayAPIError(
                f"Razorpay API connection failed: {exc.reason}"
            ) from exc

        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RazorpayAPIError("Razorpay API returned invalid JSON.") from exc

    def create_order(
        self,
        *,
        amount: Decimal | int | float | str,
        receipt: str,
        notes: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        paise = self.amount_to_paise(amount)

        if paise <= 0:
            raise ValueError("Razorpay orders cannot be created for ₹0.")

        payload: dict[str, Any] = {
            "amount": paise,
            "currency": RAZORPAY_CURRENCY,
            "receipt": receipt,
            "payment_capture": 1,
        }

        if notes:
            payload["notes"] = notes

        return self._request(
            method="POST",
            path="/orders",
            payload=payload,
        )

    @staticmethod
    def verify_payment_signature(
        *,
        order_id: str,
        payment_id: str,
        signature: str,
    ) -> None:
        if not RAZORPAY_KEY_SECRET:
            raise RazorpayConfigurationError("RAZORPAY_KEY_SECRET is not configured.")

        message = (f"{order_id}|{payment_id}").encode()

        expected = hmac.new(
            RAZORPAY_KEY_SECRET.encode("utf-8"),
            message,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(
            expected,
            signature,
        ):
            raise RazorpaySignatureError(
                "Razorpay payment signature verification failed."
            )

    @staticmethod
    def verify_webhook_signature(
        *,
        body: bytes,
        signature: str,
    ) -> None:
        if not RAZORPAY_WEBHOOK_SECRET:
            raise RazorpayConfigurationError(
                "RAZORPAY_WEBHOOK_SECRET is not configured."
            )

        expected = hmac.new(
            RAZORPAY_WEBHOOK_SECRET.encode("utf-8"),
            body,
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(
            expected,
            signature,
        ):
            raise RazorpayWebhookSignatureError(
                "Razorpay webhook signature verification failed."
            )


__all__ = ("RazorpayGateway",)
