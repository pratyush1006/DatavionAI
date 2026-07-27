"""
Audit type definitions for DatavionOS.

Provides reusable type aliases shared across the audit framework.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any, TypeAlias

###############################################################################
# Audit Identity
###############################################################################

AuditID: TypeAlias = str

AuditAction: TypeAlias = str

AuditCategory: TypeAlias = str

AuditResource: TypeAlias = str


###############################################################################
# Actor Identity
###############################################################################

ActorID: TypeAlias = str | int | None


TenantID: TypeAlias = str | int | None


OrganizationID: TypeAlias = str | int | None


###############################################################################
# Audit Data
###############################################################################

AuditMetadata: TypeAlias = Mapping[
    str,
    Any,
]


AuditChanges: TypeAlias = Mapping[
    str,
    Any,
]


AuditContext: TypeAlias = Mapping[
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
