"""
Permission classes for the Scrub Result module.
"""

from __future__ import annotations

from apps.common.permissions.base import BasePermission


class ClaimScrubResultPermission:
    VIEW = "claim_scrubbing.view"
    CREATE = "claim_scrubbing.create"
    UPDATE = "claim_scrubbing.update"
    DELETE = "claim_scrubbing.delete"


class CanViewClaimScrubResult(BasePermission):
    permission_code = ClaimScrubResultPermission.VIEW


class CanCreateClaimScrubResult(BasePermission):
    permission_code = ClaimScrubResultPermission.CREATE


class CanUpdateClaimScrubResult(BasePermission):
    permission_code = ClaimScrubResultPermission.UPDATE


class CanDeleteClaimScrubResult(BasePermission):
    permission_code = ClaimScrubResultPermission.DELETE


__all__ = [
    "CanCreateClaimScrubResult",
    "CanDeleteClaimScrubResult",
    "CanUpdateClaimScrubResult",
    "CanViewClaimScrubResult",
    "ClaimScrubResultPermission",
]
