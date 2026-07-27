"""
Notification constants for DatavionOS.

Defines framework-wide constants for notification channels,
delivery lifecycle, and priority handling.
"""

from __future__ import annotations

###############################################################################
# Notification Channels
###############################################################################

CHANNEL_EMAIL = "email"

CHANNEL_SMS = "sms"

CHANNEL_PUSH = "push"

CHANNEL_IN_APP = "in_app"

CHANNEL_WEBHOOK = "webhook"


###############################################################################
# Delivery Status
###############################################################################

STATUS_PENDING = "pending"

STATUS_QUEUED = "queued"

STATUS_SENT = "sent"

STATUS_DELIVERED = "delivered"

STATUS_FAILED = "failed"

STATUS_CANCELLED = "cancelled"


###############################################################################
# Notification Priority
###############################################################################

PRIORITY_LOW = "low"

PRIORITY_NORMAL = "normal"

PRIORITY_HIGH = "high"

PRIORITY_CRITICAL = "critical"


###############################################################################
# Default Values
###############################################################################

DEFAULT_CHANNEL = CHANNEL_IN_APP

DEFAULT_STATUS = STATUS_PENDING

DEFAULT_PRIORITY = PRIORITY_NORMAL


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "CHANNEL_EMAIL",
    "CHANNEL_IN_APP",
    "CHANNEL_PUSH",
    "CHANNEL_SMS",
    "CHANNEL_WEBHOOK",
    "DEFAULT_CHANNEL",
    "DEFAULT_PRIORITY",
    "DEFAULT_STATUS",
    "PRIORITY_CRITICAL",
    "PRIORITY_HIGH",
    "PRIORITY_LOW",
    "PRIORITY_NORMAL",
    "STATUS_CANCELLED",
    "STATUS_DELIVERED",
    "STATUS_FAILED",
    "STATUS_PENDING",
    "STATUS_QUEUED",
    "STATUS_SENT",
)
