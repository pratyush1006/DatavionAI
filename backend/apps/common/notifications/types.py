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
    TypeAlias,
)

###############################################################################
# Notification Identity
###############################################################################

NotificationID: TypeAlias = str

NotificationName: TypeAlias = str


###############################################################################
# Notification Channels
###############################################################################

NotificationChannel: TypeAlias = str


###############################################################################
# Notification Payload
###############################################################################

NotificationPayload: TypeAlias = Mapping[
    str,
    Any,
]


NotificationMetadata: TypeAlias = Mapping[
    str,
    Any,
]


###############################################################################
# Recipient Types
###############################################################################

RecipientID: TypeAlias = str | int


RecipientAddress: TypeAlias = str


###############################################################################
# Template Types
###############################################################################

TemplateName: TypeAlias = str


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
