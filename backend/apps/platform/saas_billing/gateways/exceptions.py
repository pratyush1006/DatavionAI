"""
Razorpay gateway exceptions for DatavionOS SaaS billing.
"""

from __future__ import annotations


class RazorpayGatewayError(RuntimeError):
    """Base Razorpay gateway error."""


class RazorpayConfigurationError(RazorpayGatewayError):
    """Razorpay configuration is missing or invalid."""


class RazorpayAPIError(RazorpayGatewayError):
    """Razorpay API returned an error."""


class RazorpaySignatureError(RazorpayGatewayError):
    """Razorpay checkout signature validation failed."""


class RazorpayWebhookSignatureError(RazorpayGatewayError):
    """Razorpay webhook signature validation failed."""


__all__ = (
    "RazorpayGatewayError",
    "RazorpayConfigurationError",
    "RazorpayAPIError",
    "RazorpaySignatureError",
    "RazorpayWebhookSignatureError",
)
