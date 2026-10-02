"""
Razorpay configuration for DatavionOS.

Secrets are intentionally read from environment variables.

Required:
    RAZORPAY_KEY_ID
    RAZORPAY_KEY_SECRET
    RAZORPAY_WEBHOOK_SECRET

Optional:
    RAZORPAY_ENABLED
    RAZORPAY_CURRENCY
    RAZORPAY_WEBHOOK_TOLERANCE_SECONDS
"""

from __future__ import annotations

from decouple import config


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default

    return value.strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }


RAZORPAY_ENABLED = _as_bool(
    config("RAZORPAY_ENABLED", default=None),
    default=False,
)

RAZORPAY_KEY_ID = config(
    "RAZORPAY_KEY_ID",
    "",
).strip()

RAZORPAY_KEY_SECRET = config(
    "RAZORPAY_KEY_SECRET",
    "",
).strip()

RAZORPAY_WEBHOOK_SECRET = config(
    "RAZORPAY_WEBHOOK_SECRET",
    "",
).strip()

RAZORPAY_CURRENCY = (
    config(
        "RAZORPAY_CURRENCY",
        "INR",
    )
    .strip()
    .upper()
)

RAZORPAY_WEBHOOK_TOLERANCE_SECONDS = config(
    "RAZORPAY_WEBHOOK_TOLERANCE_SECONDS",
    default=300,
    cast=int,
)


__all__ = (
    "RAZORPAY_ENABLED",
    "RAZORPAY_KEY_ID",
    "RAZORPAY_KEY_SECRET",
    "RAZORPAY_WEBHOOK_SECRET",
    "RAZORPAY_CURRENCY",
    "RAZORPAY_WEBHOOK_TOLERANCE_SECONDS",
)
