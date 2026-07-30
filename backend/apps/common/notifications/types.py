"""
Notification type definitions for DatavionOS.

Provides reusable type aliases shared across the notification
framework.
"""

from __future__ import annotations

from collections.abc import (
    Mapping,
)
from typing import (
    Any,
)

###############################################################################
# Notification Identity
###############################################################################

type NotificationID = str

type NotificationName = str


###############################################################################
# Notification Channels
###############################################################################

type NotificationChannel = str


###############################################################################
# Notification Payload
###############################################################################

type NotificationPayload = Mapping[
    str,
    Any,
]


type NotificationMetadata = Mapping[
    str,
    Any,
]


###############################################################################
# Recipient Types
###############################################################################

type RecipientID = str | int


type RecipientAddress = str


###############################################################################
# Template Types
###############################################################################

type TemplateName = str


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "NotificationChannel",
    "NotificationID",
    "NotificationMetadata",
    "NotificationName",
    "NotificationPayload",
    "RecipientAddress",
    "RecipientID",
    "TemplateName",
)
