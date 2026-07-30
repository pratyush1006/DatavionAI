"""
Audit type definitions for DatavionOS.

Provides reusable type aliases shared across the audit framework.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

###############################################################################
# Audit Identity
###############################################################################

type AuditID = str

type AuditAction = str

type AuditCategory = str

type AuditResource = str


###############################################################################
# Actor Identity
###############################################################################

type ActorID = str | int | None


type TenantID = str | int | None


type OrganizationID = str | int | None


###############################################################################
# Audit Data
###############################################################################

type AuditMetadata = Mapping[
    str,
    Any,
]


type AuditChanges = Mapping[
    str,
    Any,
]


type AuditContext = Mapping[
    str,
    Any,
]


###############################################################################
# Public Exports
###############################################################################

__all__: tuple[str, ...] = (
    "ActorID",
    "AuditAction",
    "AuditCategory",
    "AuditChanges",
    "AuditContext",
    "AuditID",
    "AuditMetadata",
    "AuditResource",
    "OrganizationID",
    "TenantID",
)
