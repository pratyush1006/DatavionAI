"""
DatavionAI API Webhook Constants.

Centralized webhook constants used throughout the DatavionAI platform.

This module defines webhook event metadata, delivery states,
signature algorithms, retry policies, payload keys, and reserved
header values.

Design Principles
-----------------
- Immutable constants
- Framework agnostic
- Provider agnostic
- No business logic
- Safe to import everywhere
"""

from __future__ import annotations

from enum import StrEnum
from typing import Final

###############################################################################
# Webhook Events
###############################################################################


class WebhookEventType(StrEnum):
    """
    Generic webhook event types.
    """

    CREATED = "created"

    UPDATED = "updated"

    DELETED = "deleted"

    RESTORED = "restored"

    ACTIVATED = "activated"

    DEACTIVATED = "deactivated"

    FAILED = "failed"


SUPPORTED_WEBHOOK_EVENTS: Final[tuple[str, ...]] = tuple(
    event.value for event in WebhookEventType
)

###############################################################################
# Delivery Status
###############################################################################


class WebhookDeliveryStatus(StrEnum):
    """
    Webhook delivery lifecycle.
    """

    PENDING = "pending"

    PROCESSING = "processing"

    DELIVERED = "delivered"

    FAILED = "failed"

    RETRYING = "retrying"

    EXPIRED = "expired"


SUPPORTED_DELIVERY_STATUSES: Final[tuple[str, ...]] = tuple(
    status.value for status in WebhookDeliveryStatus
)

###############################################################################
# Signature Algorithms
###############################################################################


class WebhookSignatureAlgorithm(StrEnum):
    """
    Supported webhook signing algorithms.
    """

    SHA256 = "sha256"

    SHA512 = "sha512"


DEFAULT_SIGNATURE_ALGORITHM: Final[str] = WebhookSignatureAlgorithm.SHA256.value

###############################################################################
# Payload Keys
###############################################################################

KEY_EVENT: Final[str] = "event"

KEY_EVENT_ID: Final[str] = "event_id"

KEY_EVENT_TYPE: Final[str] = "event_type"

KEY_DELIVERY_ID: Final[str] = "delivery_id"

KEY_TIMESTAMP: Final[str] = "timestamp"

KEY_ATTEMPT: Final[str] = "attempt"

KEY_DATA: Final[str] = "data"

KEY_SIGNATURE: Final[str] = "signature"

KEY_VERSION: Final[str] = "version"

###############################################################################
# Retry Policy Defaults
###############################################################################

DEFAULT_MAX_RETRIES: Final[int] = 5

DEFAULT_INITIAL_RETRY_DELAY_SECONDS: Final[int] = 30

DEFAULT_MAX_RETRY_DELAY_SECONDS: Final[int] = 3600

###############################################################################
# Retry Backoff Strategy
###############################################################################


class RetryStrategy(StrEnum):
    """
    Supported retry strategies.
    """

    FIXED = "fixed"

    LINEAR = "linear"

    EXPONENTIAL = "exponential"


DEFAULT_RETRY_STRATEGY: Final[str] = RetryStrategy.EXPONENTIAL.value

###############################################################################
# Reserved Payload Keys
###############################################################################

RESERVED_WEBHOOK_FIELDS: Final[frozenset[str]] = frozenset(
    {
        KEY_EVENT,
        KEY_EVENT_ID,
        KEY_EVENT_TYPE,
        KEY_DELIVERY_ID,
        KEY_TIMESTAMP,
        KEY_ATTEMPT,
        KEY_DATA,
        KEY_SIGNATURE,
        KEY_VERSION,
    }
)

###############################################################################
# Public Exports
###############################################################################

__all__ = tuple(name for name, value in globals().items() if name.isupper()) + (
    "RetryStrategy",
    "WebhookDeliveryStatus",
    "WebhookEventType",
    "WebhookSignatureAlgorithm",
)
